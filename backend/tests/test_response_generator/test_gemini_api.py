import os
from unittest.mock import MagicMock, patch

from modules.response_generator.gemini_api import GeminiResponseGenerator
from modules.schema import ChatMessage, ChatModel, ChatModelParameter


class TestGeminiResponseGenerator:
    """GeminiResponseGeneratorクラスのテスト"""

    def setup_method(self):
        """テストメソッドのセットアップ"""
        # 環境変数を設定
        self.original_gemini_model = os.getenv("GEMINI_MODEL")
        os.environ["GEMINI_MODEL"] = "gemini-2.5-flash-lite"

        # GeminiResponseGeneratorのインスタンスを作成
        self.gemini_response_generator = GeminiResponseGenerator()

    def teardown_method(self):
        """テストメソッドの teardown"""
        # 環境変数を元に戻す
        if self.original_gemini_model is not None:
            os.environ["GEMINI_MODEL"] = self.original_gemini_model
        elif "GEMINI_MODEL" in os.environ:
            del os.environ["GEMINI_MODEL"]

    def test_init(self):
        """__init__メソッドのテスト"""
        assert self.gemini_response_generator.name == ChatModel.GEMINI
        assert self.gemini_response_generator.is_use == True
        assert self.gemini_response_generator.model_name == "gemini-2.5-flash-lite"
        assert self.gemini_response_generator.llm is None
        assert self.gemini_response_generator.temperature == 0.1
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
            model="gemini-2.5-flash-lite",
            temperature=0.1,
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
        assert parameters.temperature == 0.1
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
        # モックオブジェクトを設定
        mock_response = MagicMock()
        mock_response.content = "Hello, how can I help you?"
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_google_generative_ai.return_value = mock_llm_instance

        # setupメソッドを呼び出す
        self.gemini_response_generator.setup()

        # 入力メッセージを作成
        input_messages = [ChatMessage(role="user", content="Hello")]

        # __call__メソッドを呼び出す
        response = self.gemini_response_generator(input_messages)

        # 結果を検証
        assert response == "Hello, how can I help you?"
        mock_llm_instance.invoke.assert_called_once_with(input_messages)
