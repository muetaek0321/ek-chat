import logging
from unittest.mock import MagicMock

from fastapi import Request

from modules.logger import get_endpoint_logger, get_logger, logging_config


class TestLogger:
    """logger.pyのテスト"""

    def test_logging_config_debug(self, caplog):
        """logging_config関数のテスト (デバッグモード)"""
        # デバッグモードでロギングを設定
        logging_config(debug=True)

        # ログレベルを確認
        assert logging.getLogger().level == logging.DEBUG

        # 特定のロガーのログレベルを確認
        assert logging.getLogger("httpcore").level == logging.WARNING
        assert logging.getLogger("httpx").level == logging.WARNING
        assert logging.getLogger("google_genai").level == logging.WARNING

    def test_logging_config_info(self, caplog):
        """logging_config関数のテスト (インフォモード)"""
        # インフォモードでロギングを設定
        logging_config(debug=False)

        # ログレベルを確認
        assert logging.getLogger().level == logging.INFO

        # 特定のロガーのログレベルを確認
        assert logging.getLogger("httpcore").level == logging.WARNING
        assert logging.getLogger("httpx").level == logging.WARNING
        assert logging.getLogger("google_genai").level == logging.WARNING

    def test_get_logger(self):
        """get_logger関数のテスト"""
        # ロガーを取得
        logger = get_logger("test_logger")

        # 結果を検証
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_get_endpoint_logger(self):
        """get_endpoint_logger関数のテスト"""
        # モックのRequestオブジェクトを作成
        mock_request = MagicMock(spec=Request)
        mock_request.url.path = "/api/v1/test"

        # APIエンドポイント用のロガーを取得
        logger = get_endpoint_logger(mock_request)

        # 結果を検証
        assert isinstance(logger, logging.Logger)
        assert logger.name == "/api/v1/test"
