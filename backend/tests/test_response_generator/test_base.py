import logging
from unittest.mock import MagicMock

import pytest

from modules.response_generator.base import ResponseGenerator
from modules.schema import ChatModel, ChatModelParameter


# テスト用のダミーサブクラスを作成
class DummyResponseGenerator(ResponseGenerator):
    def setup(self) -> None:
        return super().setup()

    def cleanup(self) -> None:
        return super().cleanup()

    def get_parameters(self) -> ChatModelParameter | None:
        return super().get_parameters()

    def update_parameters(self, parameters: ChatModelParameter) -> None:
        return super().update_parameters(parameters)

    def __call__(self, messages: list[dict[str, str]]) -> str:
        return super().__call__(messages)


class TestResponseGenerator:
    """ResponseGeneratorクラスのテスト"""

    def test_init(self):
        """__init__メソッドのテスト"""
        # モックのloggerオブジェクトを作成
        mock_logger = MagicMock(spec=logging.Logger)

        # ResponseGeneratorのインスタンスを作成
        response_generator = DummyResponseGenerator(mock_logger, ChatModel.GEMINI, True)

        # 結果を検証
        assert response_generator.logger == mock_logger
        assert response_generator.name == ChatModel.GEMINI
        assert response_generator.is_use == True

    def test_abstract_methods(self):
        """抽象メソッドのテスト"""
        # モックのloggerオブジェクトを作成
        mock_logger = MagicMock(spec=logging.Logger)

        # ResponseGeneratorのインスタンスを作成
        response_generator = DummyResponseGenerator(mock_logger, ChatModel.GEMINI, True)

        # 抽象メソッドを呼び出すとNotImplementedErrorが発生することを確認
        with pytest.raises(NotImplementedError):
            response_generator.setup()

        with pytest.raises(NotImplementedError):
            response_generator.cleanup()

        with pytest.raises(NotImplementedError):
            response_generator.get_parameters()

        with pytest.raises(NotImplementedError):
            response_generator.update_parameters(
                ChatModelParameter(temperature=0.5, thinking="medium")
            )

        with pytest.raises(NotImplementedError):
            response_generator([{"role": "user", "content": "Hello"}])
