import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import torch

from modules.response_generator.gemma4_12b import Gemma4LlmmaCppResponseGenerator
from schemas.chat import ChatMessage, ChatModel, ChatModelParameter, ChatOptions


class TestGemma4LlmmaCppResponseGenerator:
    """Gemma4LlmmaCppResponseGeneratorクラスのテスト"""

    def setup_method(self):
        """テストメソッドのセットアップ"""
        # 環境変数を設定
        self.original_data_dir = os.getenv("DATA_DIR")
        os.environ["DATA_DIR"] = "./develop"

        # Gemma4LlmmaCppResponseGeneratorのインスタンスを作成
        self.gemma4_llamacpp_response_generator = Gemma4LlmmaCppResponseGenerator(
            vectordb=None, extractor=None
        )

    def teardown_method(self):
        """テストメソッドの teardown"""
        # 環境変数を元に戻す
        if self.original_data_dir is not None:
            os.environ["DATA_DIR"] = self.original_data_dir
        elif "DATA_DIR" in os.environ:
            del os.environ["DATA_DIR"]

    def test_init(self):
        """__init__メソッドのテスト"""
        assert self.gemma4_llamacpp_response_generator.name == ChatModel.GEMMA4_12B
        assert self.gemma4_llamacpp_response_generator.is_use == torch.cuda.is_available()
        assert self.gemma4_llamacpp_response_generator.target_model_id == Path(
            "./develop/models/gemma-4-12B-it-qat-q4_0-gguf/gemma-4-12b-it-qat-q4_0.gguf"
        )
        assert self.gemma4_llamacpp_response_generator.max_tokens == 1024
        assert self.gemma4_llamacpp_response_generator.processor is None
        assert self.gemma4_llamacpp_response_generator.target_model is None
        assert self.gemma4_llamacpp_response_generator.temperature == 0.0

    @patch("modules.response_generator.gemma4_12b.ChatLlamaCpp")
    def test_setup(self, mock_chat_llama_cpp):
        """setupメソッドのテスト"""
        # モックオブジェクトを設定
        mock_llm_instance = MagicMock()
        mock_chat_llama_cpp.return_value = mock_llm_instance

        # setupメソッドを呼び出す
        self.gemma4_llamacpp_response_generator.setup()

        # 結果を検証
        mock_chat_llama_cpp.assert_called_once_with(
            model_path=str(
                Path("./develop/models/gemma-4-12B-it-qat-q4_0-gguf/gemma-4-12b-it-qat-q4_0.gguf")
            ),
            max_tokens=1024,
            temperature=0.0,
            n_ctx=8192,
            n_gpu_layers=-1,
            n_batch=1024,
            verbose=True,
        )
        assert self.gemma4_llamacpp_response_generator.llm == mock_llm_instance

    def test_cleanup(self):
        """cleanupメソッドのテスト"""
        # モックのLLMオブジェクトを作成
        mock_llm = MagicMock()
        mock_llm.client = MagicMock()
        self.gemma4_llamacpp_response_generator.llm = mock_llm

        # cleanupメソッドを呼び出す
        self.gemma4_llamacpp_response_generator.cleanup()

        # 結果を検証
        assert self.gemma4_llamacpp_response_generator.llm is None
        mock_llm.client.close.assert_called_once()

    def test_get_parameters(self):
        """get_parametersメソッドのテスト"""
        # get_parametersメソッドを呼び出す
        self.gemma4_llamacpp_response_generator.is_use = True
        parameters = self.gemma4_llamacpp_response_generator.get_parameters()

        # 結果を検証
        assert isinstance(parameters, ChatModelParameter)
        assert parameters.temperature == 0.0
        assert parameters.thinking is None

    def test_update_parameters(self):
        """update_parametersメソッドのテスト"""
        # 新しいパラメータを作成
        new_parameters = ChatModelParameter(temperature=0.5, thinking=None)

        # update_parametersメソッドを呼び出す
        self.gemma4_llamacpp_response_generator.update_parameters(new_parameters)

        # 結果を検証
        assert self.gemma4_llamacpp_response_generator.temperature == 0.5

    @patch("modules.response_generator.gemma4_12b.ChatLlamaCpp")
    def test_call(self, mock_chat_llama_cpp):
        """__call__メソッドのテスト"""
        # モックオブジェクトを設定
        mock_response = MagicMock()
        mock_response.content = "Hello, how can I help you?"
        mock_response.response_metadata = {}
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_llama_cpp.return_value = mock_llm_instance

        # setupメソッドを呼び出す
        self.gemma4_llamacpp_response_generator.setup()

        # 入力メッセージを作成
        user_message = ChatMessage(role="user", content="Hello")
        options = ChatOptions(is_rag_enabled=False)
        self.gemma4_llamacpp_response_generator.convert_input_messages = MagicMock(
            return_value=[{"role": "user", "content": "Hello"}]
        )

        # __call__メソッドを呼び出す
        response, metadata = self.gemma4_llamacpp_response_generator([], user_message, options)

        # 結果を検証
        assert response == "Hello, how can I help you?"
        mock_llm_instance.invoke.assert_called_once_with([{"role": "user", "content": "Hello"}])
