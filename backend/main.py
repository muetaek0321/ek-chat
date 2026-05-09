import logging
import os
from typing import Annotated

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse

from modules.chat_manager import ChatManager
from modules.logger import get_endpoint_logger, logging_config
from modules.schema import (
    ChatHistory,
    ChatId,
    ChatInfo,
    ChatInfoList,
    ChatMessage,
    GenerateChatResponse,
)

# .envファイルから環境変数を読み込む
load_dotenv()

# ロガーのインスタンスを取得
logging_config(debug=(os.getenv("ENVIRON", "prod") == "dev"))

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# ChatManagerのインスタンスを作成
chat = ChatManager()


@app.get(
    "/",
    response_class=RedirectResponse,
    summary="SwaggerUIにRedirect",
    description="ルートエンドポイント: SwaggerUIにRedirectする",
)
def root() -> RedirectResponse:
    """ルートエンドポイント: SwaggerUIにRedirect

    Returns:
        RedirectResponse: SwaggerUIへのリダイレクトレスポンス
    """

    return RedirectResponse(url="/docs")


@app.get(
    "/init",
    response_model=ChatInfoList,
    summary="アプリの初期データを取得",
    description="チャットボットアプリの初期データを取得するエンドポイント",
)
async def init_app(
    logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatInfoList:
    """チャットボットアプリの初期データを取得

    Args:
        logger (logging.Logger): エンドポイント用のロガー

    Returns:
        ChatInfoList: チャット一覧のデータ
    """
    logger.debug("アプリの初期データを取得します")

    # 保存済みのチャット一覧を取得
    chat_info_list = chat.load_chat_list()

    return chat_info_list


@app.put(
    "/new",
    response_model=ChatInfo,
    summary="新しいチャットを作成",
    description="新しいチャットを作成するエンドポイント",
)
async def create_new_chat(
    logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatInfo:
    """新しいチャットを作成

    Args:
        logger (logging.Logger): エンドポイント用のロガー

    Returns:
        ChatInfo: 作成された新しいチャットの情報
    """
    logger.debug("新しいチャットを作成します")

    # 新しいチャットを作成
    new_chat_info = chat.new_chat()

    return new_chat_info


@app.get(
    "/history",
    response_model=ChatHistory,
    summary="チャットの履歴を取得",
    description="チャットIDを指定して対応するチャットの履歴を取得するエンドポイント",
)
async def get_chat_history(
    query: Annotated[ChatId, Depends()],
    logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatHistory:
    """チャットの履歴を取得

    Args:
        query (ChatId): クエリパラメータ（チャットID）
        logger (logging.Logger): エンドポイント用のロガー

    Returns:
        ChatHistory: 指定されたチャットIDのチャット履歴データ
    """
    chat_id = query.chat_id
    logger.debug(f"チャットID: {chat_id}")

    # チャットの履歴を取得
    chat_history = chat.load_chat_history(chat_id=chat_id)

    return chat_history


@app.post(
    "/chat",
    response_model=GenerateChatResponse,
    summary="userの入力に対してassistantの応答を生成",
    description="アプリでのuserの入力に対してassistant（生成AI）の応答を生成するエンドポイント",
)
async def generate_chat_response(
    chat_message: ChatMessage, logger: Annotated[logging.Logger, Depends(get_endpoint_logger)]
) -> GenerateChatResponse:
    """userの入力に対してassistantの生成

    Args:
        chat_message (ChatMessage): リクエストボディ（ユーザが入力したメッセージ）
        logger (logging.Logger): エンドポイント用のロガー

    Returns:
        GenerateChatResponse: 生成した返答文のデータとチャット情報
    """
    logger.debug(chat_message.model_dump())

    # 返答を生成
    response = chat.generate(user_message=chat_message)

    return response


if __name__ == "__main__":
    uvicorn.run(app)
