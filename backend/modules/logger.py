import logging

from fastapi import Request


def logging_config(debug: bool) -> None:
    """ロギングの設定を行う関数

    Args:
        debug (bool): デバッグモードかどうか
    """
    # ロギングの基本設定
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    # ロガーレベルの個別設定
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google_genai").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """ロガーを取得する関数

    Args:
        name (str): ロガーの名前

    Returns:
        logging.Logger: ロガーのインスタンス
    """
    return logging.getLogger(name)


def get_endpoint_logger(req: Request) -> logging.Logger:
    """APIエンドポイント用のロガーを取得する関数

    Args:
        req (Request): APIエンドポイントのRequestオブジェクト

    Returns:
        logging.Logger: APIエンドポイント用のロガーのインスタンス
    """
    endpoint_name = req.url.path
    return get_logger(endpoint_name)
