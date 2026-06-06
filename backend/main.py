import logging
import os
from typing import Annotated

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

from modules.chat_manager import ChatManager
from modules.logger import get_endpoint_logger, get_logger, logging_config
from modules.schema import (
    ChatHistory,
    ChatId,
    ChatInfo,
    ChatInfoList,
    ChatMessage,
    GenerateChatResponse,
    SelectedChatModel,
    SettingsResponse,
    SystemPromptText,
)

# .envファイルから環境変数を読み込む
load_dotenv()

# ロガーのインスタンスを取得
logging_config(debug=(os.getenv("ENVIRON", "prod") == "dev"))
app_logger = get_logger(__name__)

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# ChatManagerのインスタンスを作成
chat = ChatManager()


@app.exception_handler(HTTPException)
async def http_exception_handler(
    req: Request,
    exc: HTTPException,
) -> JSONResponse:
    """HTTPExceptionのエラーハンドラ

    Args:
        req (Request): 発生したHTTPエラーのリクエスト情報
        exc (HTTPException): 発生したHTTPエラーの例外オブジェクト

    Returns:
        JSONResponse: エラーレスポンス（HTTPステータスコードとエラーメッセージを含むJSON形式のレスポンス）
    """
    app_logger.error(
        f"HTTP error: method={req.method} path={req.url.path} status={exc.status_code} detail={exc.detail}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail}),
    )


@app.exception_handler(Exception)
async def other_exception_handler(
    req: Request,
    exc: Exception,
) -> JSONResponse:
    """その他の例外のエラーハンドラ

    Args:
        req (Request): 発生したエラーのリクエスト情報
        exc (Exception): 発生したエラーの例外オブジェクト

    Returns:
        JSONResponse: エラーレスポンス（HTTPステータスコード500とエラーメッセージを含むJSON形式のレスポンス）
    """
    app_logger.error(f"Error: method={req.method} path={req.url.path} detail={exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": f"Internal server error: {exc}"}),
    )


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
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatInfoList:
    """チャットボットアプリの初期データを取得

    Args:
        api_logger (logging.Logger): エンドポイント用のロガー

    Returns:
        ChatInfoList: チャット一覧のデータ
    """
    api_logger.debug("アプリの初期データを取得します")

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
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatInfo:
    """新しいチャットを作成

    Args:
        api_logger (logging.Logger): エンドポイント用のロガー

    Returns:
        ChatInfo: 作成された新しいチャットの情報
    """
    api_logger.debug("新しいチャットを作成します")

    # 新しいチャットを作成
    new_chat_info = chat.new_chat()

    return new_chat_info


@app.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="チャットを削除",
    description="指定したIDのチャットを削除",
)
async def delete_chat(
    query: Annotated[ChatId, Depends()],
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> None:
    """チャットを削除

    Args:
        query (ChatId): クエリパラメータ（チャットID）
        api_logger (logging.Logger): エンドポイント用のロガー
    """
    chat_id = query.chat_id
    api_logger.debug(f"チャットを削除します: {chat_id}")

    # チャットの削除
    chat.delete_chat(chat_id)


@app.get(
    "/history",
    response_model=ChatHistory,
    summary="チャットの履歴を取得",
    description="チャットIDを指定して対応するチャットの履歴を取得するエンドポイント",
)
async def get_chat_history(
    query: Annotated[ChatId, Depends()],
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatHistory:
    """チャットの履歴を取得

    Args:
        query (ChatId): クエリパラメータ（チャットID）
        api_logger (logging.Logger): エンドポイント用のロガー

    Returns:
        ChatHistory: 指定されたチャットIDのチャット履歴データ
    """
    chat_id = query.chat_id
    api_logger.debug(f"チャットID: {chat_id}")

    # チャットの履歴を取得
    chat_history = chat.load_chat_history(chat_id=chat_id)

    return chat_history


@app.get(
    "/settings",
    response_model=SettingsResponse,
    summary="設定項目のデータを取得",
    description="SystemPromptと設定されたモデルのデータを取得するエンドポイント",
)
async def get_settings(
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> SettingsResponse:
    """設定項目のデータを取得"""
    api_logger.debug("設定項目のデータを取得します")

    # 設定を取得
    system_prompt = chat.get_system_prompt()
    chat_model_info_list = chat.get_chat_model_info()

    # レスポンスデータを作成
    response = SettingsResponse(
        system_prompt=system_prompt,
        chat_model_info_list=chat_model_info_list,
    )

    return response


@app.patch(
    "/system_prompt",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="SystemPromptのテキストを作成/更新",
    description="SystemPromptのテキストを作成または更新するエンドポイント",
)
async def update_system_prompt(
    system_prompt: SystemPromptText,
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> None:
    """SystemPromptを作成/更新"""
    system_prompt_text = system_prompt.text
    api_logger.debug(f"SystemPrompt: {system_prompt_text[:10]}...")

    # SystemPromptを作成/更新し登録
    chat.update_system_prompt(system_prompt_text)


@app.patch(
    "/model",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="選択されたモデルに変更し設定を適用",
    description="選択されたモデルに変更し設定を適用するエンドポイント",
)
async def select_chat_model(
    chat_model: SelectedChatModel,
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> None:
    """選択されたモデルに変更し設定を適用"""
    selected_chat_model = chat_model.model
    parameters = chat_model.parameters
    api_logger.debug(f"モデル: {selected_chat_model.value} パラメータ: {parameters.model_dump()}")

    # 選択されたモデルに変更し設定を適用
    chat.change_chat_model(selected_chat_model, parameters)


@app.post(
    "/chat",
    response_model=GenerateChatResponse,
    summary="userの入力に対してassistantの応答を生成",
    description="アプリでのuserの入力に対してassistant（生成AI）の応答を生成するエンドポイント",
)
async def generate_chat_response(
    chat_message: ChatMessage, api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)]
) -> GenerateChatResponse:
    """userの入力に対してassistantの生成

    Args:
        chat_message (ChatMessage): リクエストボディ（ユーザが入力したメッセージ）
        api_logger (logging.Logger): エンドポイント用のロガー

    Returns:
        GenerateChatResponse: 生成した返答文のデータとチャット情報
    """
    api_logger.debug(chat_message.model_dump())

    # 返答を生成
    response = chat.generate(user_message=chat_message)

    return response


if __name__ == "__main__":
    uvicorn.run(app)
