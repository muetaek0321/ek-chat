import logging
import os
from typing import Annotated

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse

from modules.chat_manager import ChatManager
from modules.logger import get_endpoint_logger, logging_config
from modules.schema import ChatMessage

# .envファイルから環境変数を読み込む
load_dotenv()

# ロガーのインスタンスを取得
logging_config(debug=(os.getenv("ENVIRON", "prod") == "dev"))

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# ChatManagerのインスタンスを作成
chat = ChatManager()


@app.get("/", response_class=RedirectResponse)
def root() -> RedirectResponse:
    """ルートエンドポイント: SwaggerUIにRedirectする"""

    return RedirectResponse(url="/docs")


@app.post("/chat", response_model=ChatMessage)
def generate_chat_response(
    payload: ChatMessage, logger: Annotated[logging.Logger, Depends(get_endpoint_logger)]
) -> ChatMessage:
    """userの入力に対してassistantの応答を返す"""
    chat_message = payload.model_dump()
    logger.debug(chat_message)

    # 返答を生成
    response = chat.generate(user_message=chat_message)

    return response


if __name__ == "__main__":
    uvicorn.run(app)
