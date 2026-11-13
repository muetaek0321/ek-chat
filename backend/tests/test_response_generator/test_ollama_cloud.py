import os
import shutil
from unittest.mock import MagicMock, patch

from modules.response_generator.ollama_cloud import OllamaCloudResponseGenerator
from schemas.chat import ChatMessage, ChatModel, ChatModelParameter, ChatOptions


class TestOllamaCloudResponseGenerator:
    """OllamaCloudResponseGeneratorクラスのテスト"""

    def setup_method(self):
        """テストメソッドのセットアップ"""
        # 環境変数を設定
        self.original_ollama_model = os.getenv("OLLAMA_CLOUD_MODEL")
        self.original_ollama_api_key = os.getenv("OLLAMA_API_KEY")
        os.environ["OLLAMA_CLOUD_MODEL"] = "gpt-oss:120b"
        os.environ["OLLAMA_API_KEY"] = "test_api_key"

        # OllamaCloudResponseGeneratorのインスタンスを作成
        self.ollama_cloud_response_generator = OllamaCloudResponseGenerator(
            vectordb=None, extractor=None
        )

    def teardown_method(self):
        """テストメソッドの teardown"""
        # 環境変数を元に戻す
        if self.original_ollama_model is not None:
            os.environ["OLLAMA_CLOUD_MODEL"] = self.original_ollama_model
        elif "OLLAMA_CLOUD_MODEL" in os.environ:
            del os.environ["OLLAMA_CLOUD_MODEL"]

        if self.original_ollama_api_key is not None:
            os.environ["OLLAMA_API_KEY"] = self.original_ollama_api_key
        elif "OLLAMA_API_KEY" in os.environ:
            del os.environ["OLLAMA_API_KEY"]

    def test_init(self):
        """__init__メソッドのテスト"""
        assert self.ollama_cloud_response_generator.name == ChatModel.OLLAMA_CLOUD
        assert self.ollama_cloud_response_generator.is_use == bool(shutil.which("ollama"))
        assert self.ollama_cloud_response_generator.model_name == "gpt-oss:120b"
        assert self.ollama_cloud_response_generator.llm is None
        assert self.ollama_cloud_response_generator.temperature == 0.0

    @patch("modules.response_generator.ollama_cloud.ChatOllama")
    def test_setup(self, mock_chat_ollama):
        """setupメソッドのテスト"""
        # モックオブジェクトを設定
        mock_llm_instance = MagicMock()
        mock_chat_ollama.return_value = mock_llm_instance

        # setupメソッドを呼び出す
        self.ollama_cloud_response_generator.setup()

        # 結果を検証
        mock_chat_ollama.assert_called_once_with(
            model="gpt-oss:120b",
            base_url="https://ollama.com",
            api_key="test_api_key",
            temperature=0.0,
        )
        assert self.ollama_cloud_response_generator.llm == mock_llm_instance

    def test_cleanup(self):
        """cleanupメソッドのテスト"""
        # モックのLLMオブジェクトを作成
        mock_llm = MagicMock()
        self.ollama_cloud_response_generator.llm = mock_llm

        # cleanupメソッドを呼び出す
        self.ollama_cloud_response_generator.cleanup()

        # 結果を検証
        assert self.ollama_cloud_response_generator.llm is None

    def test_get_parameters(self):
        """get_parametersメソッドのテスト"""
        # get_parametersメソッドを呼び出す
        self.ollama_cloud_response_generator.is_use = True
        parameters = self.ollama_cloud_response_generator.get_parameters()

        # 結果を検証
        assert isinstance(parameters, ChatModelParameter)
        assert parameters.temperature == 0.0
        assert parameters.thinking is None

    def test_update_parameters(self):
        """update_parametersメソッドのテスト"""
        # 新しいパラメータを作成
        new_parameters = ChatModelParameter(temperature=0.5, thinking=None)

        # update_parametersメソッドを呼び出す
        self.ollama_cloud_response_generator.update_parameters(new_parameters)

        # 結果を検証
        assert self.ollama_cloud_response_generator.temperature == 0.5

    @patch("modules.response_generator.ollama_cloud.ChatOllama")
    def test_call(self, mock_chat_ollama):
        """__call__メソッドのテスト"""
        # モックオブジェクトを設定
        mock_response = MagicMock()
        mock_response.content = "Hello, how can I help you?"
        mock_response.response_metadata = {}
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_ollama.return_value = mock_llm_instance

        # setupメソッドを呼び出す
        self.ollama_cloud_response_generator.setup()

        # 入力メッセージを作成
        user_message = ChatMessage(role="user", content="Hello")
        options = ChatOptions(is_rag_enabled=False)
        self.ollama_cloud_response_generator.convert_input_messages = MagicMock(
            return_value=[{"role": "user", "content": "Hello"}]
        )

        # __call__メソッドを呼び出す
        response, metadata = self.ollama_cloud_response_generator([], user_message, options)

        # 結果を検証
        assert response == "Hello, how can I help you?"
        mock_llm_instance.invoke.assert_called_once_with([{"role": "user", "content": "Hello"}])
