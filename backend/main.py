import logging
import os
from typing import Annotated

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse

from modules.chat_manager import ChatManager
from modules.logger import get_endpoint_logger, logging_config
from modules.schema import ChatHistory, ChatId, ChatMessage

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


@app.put("/new", response_model=ChatId)
def create_new_chat(
    logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatId:
    """新しいチャットを作成"""
    logger.debug("新しいチャットを作成します")

    # 新しいチャットを作成
    chat_id = chat.new_chat()

    return ChatId(chat_id=chat_id)


@app.get("/history", response_model=ChatHistory)
def get_chat_history(
    query: Annotated[ChatId, Depends()],
    logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatHistory:
    """チャットの履歴を返す"""
    chat_id = query.chat_id
    logger.debug(f"チャットID: {chat_id}")

    # チャットの履歴を取得
    chat_history = chat.load_chat_history(chat_id=chat_id)

    return chat_history


@app.post("/chat", response_model=ChatMessage)
def generate_chat_response(
    chat_message: ChatMessage, logger: Annotated[logging.Logger, Depends(get_endpoint_logger)]
) -> ChatMessage:
    """userの入力に対してassistantの応答を返す"""
    logger.debug(chat_message.model_dump())

    # 返答を生成
    response = chat.generate(user_message=chat_message)

    return response


if __name__ == "__main__":
    uvicorn.run(app)
