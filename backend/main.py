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
    """HTTPExceptionのエラーハンドラ。

    発生したHTTPエラーのログを出力し、クライアントへエラー詳細を含むJSONレスポンスを返します。

    Args:
        req: 発生したHTTPエラーのリクエスト情報。
        exc: 発生したHTTPエラーの例外オブジェクト。

    Returns:
        HTTPステータスコードとエラーメッセージを含むJSON形式のレスポンス。
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
    """その他の予期しない例外のエラーハンドラ。

    発生したエラーの詳細ログを出力し、ステータスコード500の共通エラーレスポンスを返します。

    Args:
        req: 発生したエラーのリクエスト情報。
        exc: 発生した例外オブジェクト。

    Returns:
        HTTPステータスコード500と内部エラーメッセージを含むJSON形式のレスポンス。
    """
    app_logger.error(f"Error: method={req.method} path={req.url.path} detail={exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": "Internal server error"}),
    )


@app.get(
    "/",
    response_class=RedirectResponse,
    summary="SwaggerUIにRedirect",
)
def root() -> RedirectResponse:
    """Swagger UIへリダイレクトする。

    ルートパスへのアクセスをFastAPIのドキュメント（Swagger UI）へ転送します。

    ### レスポンス
    - **307 Temporary Redirect**: `/docs` へのリダイレクトレスポンス
    """
    return RedirectResponse(url="/docs")


@app.get(
    "/init",
    response_model=ChatInfoList,
    summary="アプリの初期データを取得",
)
async def init_app(
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatInfoList:
    """チャットボットアプリの初期データを取得する。

    保存先ディレクトリから既存のチャット一覧（チャットIDとタイトル）を読み込んで返します。

    ### 処理の流れ
    1. 保存先ディレクトリ内の全チャット履歴ファイルを走査
    2. 各チャットの最初のユーザー入力をタイトル（先頭15文字）として取得
    3. チャット一覧（`ChatInfoList`）を構築して返却
    """
    api_logger.debug("アプリの初期データを取得します")

    # 保存済みのチャット一覧を取得
    chat_info_list = chat.load_chat_list()

    return chat_info_list


@app.put(
    "/new",
    response_model=ChatInfo,
    summary="新しいチャットを作成",
)
async def create_new_chat(
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatInfo:
    """新しいチャットセッションを作成する。

    新規チャット用の状態を初期化し、初期チャット情報を返します。

    ### 処理の流れ
    1. 新規チャットID（`"new"`）とデフォルトタイトルを設定
    2. 現在のチャット履歴を初期化
    3. 新しいチャット情報（`ChatInfo`）を返却
    """
    api_logger.debug("新しいチャットを作成します")

    # 新しいチャットを作成
    new_chat_info = chat.new_chat()

    return new_chat_info


@app.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="チャットを削除",
)
async def delete_chat(
    query: Annotated[ChatId, Depends()],
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> None:
    """指定したIDのチャットを削除する。

    クエリパラメータで指定されたチャットIDの履歴ファイルを削除します。

    ### 処理の流れ
    1. クエリパラメータから対象の `chat_id` を取得
    2. `chat_id` が `"new"` 以外の場合、対応するチャット履歴ファイルを削除

    ### エラーレスポンス
    - **422 Unprocessable Entity**: クエリパラメータのバリデーションエラー
    """
    chat_id = query.chat_id
    api_logger.debug(f"チャットを削除します: {chat_id}")

    # チャットの削除
    chat.delete_chat(chat_id)


@app.get(
    "/history",
    response_model=ChatHistory,
    summary="チャットの履歴を取得",
)
async def get_chat_history(
    query: Annotated[ChatId, Depends()],
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> ChatHistory:
    """チャットのメッセージ履歴を取得する。

    指定されたチャットIDに対応する過去の対話履歴をストレージから読み込んで返します。

    ### 処理の流れ
    1. クエリパラメータから `chat_id` を取得
    2. `chat_id` が `"new"` の場合は空の履歴を返却
    3. 既存のチャットIDの場合は該当する履歴ファイルからメッセージリストを読み込み
    4. 現在選択中のチャットIDを更新し、履歴データ（`ChatHistory`）を返却

    ### エラーレスポンス
    - **422 Unprocessable Entity**: クエリパラメータのバリデーションエラー
    - **500 Internal Server Error**: 指定されたIDのチャット履歴が見つからない、または読み込みに失敗した場合
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
)
async def get_settings(
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> SettingsResponse:
    """システムプロンプトおよびモデル設定の情報を取得する。

    現在登録されているSystemPromptのテキストと、利用可能な全チャットモデルの一覧（選択状態・パラメータ含む）を返します。

    ### 処理の流れ
    1. 登録されているSystemPromptテキストを取得
    2. 各チャットモデルの利用可否、選択状態、パラメータ設定を取得
    3. 設定データ（`SettingsResponse`）を構築して返却
    """
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
)
async def update_system_prompt(
    system_prompt: SystemPromptText,
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> None:
    """SystemPromptのテキストを作成または更新する。

    リクエストボディで渡されたテキストを新しいSystemPromptとしてファイルに保存し、実行環境へ反映します。

    ### 処理の流れ
    1. リクエストボディからSystemPromptテキストを取得
    2. `system_prompt.md` ファイルへ書き込み保存
    3. チャット管理クラス内のSystemPromptを更新

    ### エラーレスポンス
    - **422 Unprocessable Entity**: リクエストボディのバリデーションエラー
    """
    system_prompt_text = system_prompt.text
    api_logger.debug(f"SystemPrompt: {system_prompt_text[:10]}...")

    # SystemPromptを作成/更新し登録
    chat.update_system_prompt(system_prompt_text)


@app.patch(
    "/model",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="選択されたモデルに変更し設定を適用",
)
async def select_chat_model(
    chat_model: SelectedChatModel,
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> None:
    """使用するチャットモデルを変更しパラメータを適用する。

    指定されたチャットモデルへ切り替え、生成パラメータ（temperature、thinking等）を更新して初期化します。

    ### 処理の流れ
    1. 現在のモデルのリソース（GPUメモリ等）を解放
    2. 指定されたチャットモデルへ切り替え
    3. パラメータを更新し、切り替え先モデルの初期化処理を実行

    ### エラーレスポンス
    - **422 Unprocessable Entity**: リクエストボディのバリデーションエラー
    """
    selected_chat_model = chat_model.model
    parameters = chat_model.parameters
    api_logger.debug(f"モデル: {selected_chat_model.value} パラメータ: {parameters.model_dump()}")

    # 選択されたモデルに変更し設定を適用
    chat.change_chat_model(selected_chat_model, parameters)


@app.post(
    "/chat",
    response_model=GenerateChatResponse,
    summary="userの入力に対してassistantの応答を生成",
)
async def generate_chat_response(
    chat_message: ChatMessage, api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)]
) -> GenerateChatResponse:
    """ユーザーの入力に対してアシスタント（生成AI）の応答を生成する。

    ユーザーのメッセージを受け取り、SystemPromptおよび過去の会話コンテキストを含めてLLMへ問い合わせ、生成された応答を返します。対話履歴は永続化されます。

    ### 処理の流れ
    1. 既存のチャット履歴にSystemPromptを結合（設定時のみ）
    2. 選択中のチャットモデルを呼び出して返答文を生成
    3. ユーザーメッセージと生成されたアシスタントメッセージを履歴に追加
    4. チャット履歴をストレージへ保存（新規チャットの場合は新しいチャットIDを発行）
    5. アシスタントメッセージと新規チャット情報を返却

    ### エラーレスポンス
    - **422 Unprocessable Entity**: リクエストボディのバリデーションエラー
    - **500 Internal Server Error**: モデル生成エラーまたはファイル保存エラー
    """
    api_logger.debug(chat_message.model_dump())

    # 返答を生成
    response = chat.generate(user_message=chat_message)

    return response


if __name__ == "__main__":
    uvicorn.run(app)
