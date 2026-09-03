from unittest.mock import MagicMock, patch

import pytest

from modules.response_generator.gemini_api import GeminiResponseGenerator
from modules.schema import ChatMessage, ChatModel, ChatModelParameter


class TestGeminiResponseGenerator:
    """GeminiResponseGeneratorクラスのテスト"""

    def setup_method(self):
        """テストメソッドのセットアップ"""
        # GeminiResponseGeneratorのインスタンスを作成
        self.gemini_response_generator = GeminiResponseGenerator()

    def test_init(self):
        """__init__メソッドのテスト"""
        assert self.gemini_response_generator.name == ChatModel.GEMINI
        assert self.gemini_response_generator.is_use
        assert self.gemini_response_generator.model_name == ""
        assert self.gemini_response_generator.model_index == 0
        assert self.gemini_response_generator.llm is None
        assert self.gemini_response_generator.temperature == 0.0
        assert self.gemini_response_generator.thinking == "medium"
        assert self.gemini_response_generator.thinking_budget_dict == {
            "low": 0,
            "medium": 1024,
            "high": 4096,
        }

    @patch("modules.response_generator.gemini_api.ChatGoogleGenerativeAI")
    def test_setup(self, mock_chat_google_generative_ai):
        """setupメソッドのテスト"""
        # モックオブジェクトを設定
        mock_llm_instance = MagicMock()
        mock_chat_google_generative_ai.return_value = mock_llm_instance

        # setupメソッドを呼び出す
        self.gemini_response_generator.setup()

        # 結果を検証
        mock_chat_google_generative_ai.assert_called_once_with(
            model="gemini-3.8-flash",
            temperature=0.0,
            thinking_budget=1024,
        )
        assert self.gemini_response_generator.llm == mock_llm_instance

    def test_cleanup(self):
        """cleanupメソッドのテスト"""
        # モックのLLMオブジェクトを作成
        mock_llm = MagicMock()
        self.gemini_response_generator.llm = mock_llm

        # cleanupメソッドを呼び出す
        self.gemini_response_generator.cleanup()

        # 結果を検証
        assert self.gemini_response_generator.llm is None

    def test_get_parameters(self):
        """get_parametersメソッドのテスト"""
        # get_parametersメソッドを呼び出す
        parameters = self.gemini_response_generator.get_parameters()

        # 結果を検証
        assert isinstance(parameters, ChatModelParameter)
        assert parameters.temperature == 0.0
        assert parameters.thinking == "medium"

    def test_update_parameters(self):
        """update_parametersメソッドのテスト"""
        # 新しいパラメータを作成
        new_parameters = ChatModelParameter(temperature=0.5, thinking="high")

        # update_parametersメソッドを呼び出す
        self.gemini_response_generator.update_parameters(new_parameters)

        # 結果を検証
        assert self.gemini_response_generator.temperature == 0.5
        assert self.gemini_response_generator.thinking == "high"

    @patch("modules.response_generator.gemini_api.ChatGoogleGenerativeAI")
    def test_call(self, mock_chat_google_generative_ai):
        """__call__メソッドのテスト"""
        mock_response = MagicMock(text="Hello, how can I help you?", response_metadata={})
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_google_generative_ai.return_value = mock_llm_instance
        formatted_messages = [MagicMock()]
        self.gemini_response_generator.convert_input_messages = MagicMock(
            return_value=formatted_messages
        )

        response, metadata = self.gemini_response_generator(
            [], ChatMessage(role="user", content="Hello")
        )

        assert response == "Hello, how can I help you?"
        assert metadata.model_name == "gemini-3.8-flash"
        mock_llm_instance.invoke.assert_called_once_with(formatted_messages)

    @patch("modules.response_generator.gemini_api.ChatGoogleGenerativeAI")
    def test_call_retries_with_next_model(self, mock_chat_google_generative_ai):
        """失敗したモデルを解放し、次のモデルで一度だけ再試行する"""
        failed_llm = MagicMock()
        failed_llm.invoke.side_effect = RuntimeError("request failed")
        mock_response = MagicMock(text="Retried response", response_metadata={})
        next_llm = MagicMock()
        next_llm.invoke.return_value = mock_response
        mock_chat_google_generative_ai.side_effect = [failed_llm, next_llm]
        formatted_messages = [MagicMock()]
        self.gemini_response_generator.convert_input_messages = MagicMock(
            return_value=formatted_messages
        )

        response, metadata = self.gemini_response_generator(
            [], ChatMessage(role="user", content="Hello")
        )

        assert response == "Retried response"
        assert metadata.model_name == "gemini-3.7-flash"
        assert self.gemini_response_generator.model_index == 1
        assert mock_chat_google_generative_ai.call_args_list[0].kwargs["model"] == "gemini-3.8-flash"
        assert mock_chat_google_generative_ai.call_args_list[1].kwargs["model"] == "gemini-3.7-flash"

    @patch("modules.response_generator.gemini_api.ChatGoogleGenerativeAI")
    def test_call_does_not_initialize_another_model_after_final_failure(
        self, mock_chat_google_generative_ai
    ):
        """最後の試行に失敗した後、不要な次モデルの初期化を行わない"""
        self.gemini_response_generator.model_list = ["first", "second"]
        mock_chat_google_generative_ai.return_value.invoke.side_effect = RuntimeError("request failed")
        self.gemini_response_generator.convert_input_messages = MagicMock(return_value=[])

        with pytest.raises(RuntimeError, match="request failed"):
            self.gemini_response_generator([], ChatMessage(role="user", content="Hello"))

        assert mock_chat_google_generative_ai.call_count == 2
        assert self.gemini_response_generator.llm is None
