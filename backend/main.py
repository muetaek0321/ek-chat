import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

# .envファイルから環境変数を読み込む
# NOTE: Router側でも環境変数を有効にするためこの段階で読み込むようにする
load_dotenv()

from modules.logger import get_logger, logging_config
from routers import chat

# ロガーのインスタンスを取得
logging_config(debug=(os.getenv("ENVIRON", "prod") == "dev"))
app_logger = get_logger(__name__)

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# Routerの設定
app.include_router(chat.router)


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


if __name__ == "__main__":
    uvicorn.run(app)
