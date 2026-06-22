import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from modules.response_generator.gemma4_e2b import Gemma4HuggingFaceResponseGenerator
from modules.schema import ChatMessage, ChatModel, ChatModelParameter


class TestGemma4HuggingFaceResponseGenerator:
    """Gemma4HuggingFaceResponseGeneratorクラスのテスト"""

    def setup_method(self):
        """テストメソッドのセットアップ"""
        # 環境変数を設定
        self.original_data_dir = os.getenv("DATA_DIR")
        os.environ["DATA_DIR"] = "./develop"

        # Gemma4HuggingFaceResponseGeneratorのインスタンスを作成
        self.gemma4_huggingface_response_generator = Gemma4HuggingFaceResponseGenerator()

    def teardown_method(self):
        """テストメソッドの teardown"""
        # 環境変数を元に戻す
        if self.original_data_dir is not None:
            os.environ["DATA_DIR"] = self.original_data_dir
        elif "DATA_DIR" in os.environ:
            del os.environ["DATA_DIR"]

    def test_init(self):
        """__init__メソッドのテスト"""
        assert self.gemma4_huggingface_response_generator.name == ChatModel.GEMMA4_E2B
        assert (
            self.gemma4_huggingface_response_generator.is_use == True
        )  # Assuming CUDA is available in test environment
        assert self.gemma4_huggingface_response_generator.target_model_id == Path(
            "./develop/models/gemma-4-E2B-it"
        )
        assert self.gemma4_huggingface_response_generator.assistant_model_id == Path(
            "./develop/models/gemma-4-E2B-it-assistant"
        )
        assert self.gemma4_huggingface_response_generator.max_new_tokens == 512
        assert self.gemma4_huggingface_response_generator.processor is None
        assert self.gemma4_huggingface_response_generator.target_model is None
        assert self.gemma4_huggingface_response_generator.assistant_model is None
        assert self.gemma4_huggingface_response_generator.temperature == 0.1

    @patch("modules.response_generator.gemma4_e2b.AutoProcessor")
    @patch("modules.response_generator.gemma4_e2b.AutoModelForCausalLM")
    def test_setup(self, mock_auto_model_for_causal_lm, mock_auto_processor):
        """setupメソッドのテスト"""
        # モックオブジェクトを設定
        mock_processor = MagicMock()
        mock_target_model = MagicMock()
        mock_assistant_model = MagicMock()
        mock_auto_processor.from_pretrained.return_value = mock_processor
        mock_auto_model_for_causal_lm.from_pretrained.side_effect = [
            mock_target_model,  # 1回目の呼び出し
            mock_assistant_model,  # 2回目の呼び出し
        ]

        # setupメソッドを呼び出す
        self.gemma4_huggingface_response_generator.setup()

        # 結果を検証
        mock_auto_processor.from_pretrained.assert_called_once_with(
            Path("./develop/models/gemma-4-E2B-it")
        )
        mock_auto_model_for_causal_lm.from_pretrained.assert_any_call(
            Path("./develop/models/gemma-4-E2B-it"),
            dtype="auto",
            device_map="auto",
        )
        mock_auto_model_for_causal_lm.from_pretrained.assert_any_call(
            Path("./develop/models/gemma-4-E2B-it-assistant"),
            dtype="auto",
            device_map="auto",
        )
        assert self.gemma4_huggingface_response_generator.processor == mock_processor
        assert self.gemma4_huggingface_response_generator.target_model == mock_target_model
        assert self.gemma4_huggingface_response_generator.assistant_model == mock_assistant_model

    def test_cleanup(self):
        """cleanupメソッドのテスト"""
        # モックのモデルとプロセッサオブジェクトを作成
        mock_target_model = MagicMock()
        mock_assistant_model = MagicMock()
        mock_processor = MagicMock()
        self.gemma4_huggingface_response_generator.target_model = mock_target_model
        self.gemma4_huggingface_response_generator.assistant_model = mock_assistant_model
        self.gemma4_huggingface_response_generator.processor = mock_processor

        # cleanupメソッドを呼び出す
        self.gemma4_huggingface_response_generator.cleanup()

        # 結果を検証
        assert self.gemma4_huggingface_response_generator.target_model is None
        assert self.gemma4_huggingface_response_generator.assistant_model is None
        assert self.gemma4_huggingface_response_generator.processor is None
        mock_target_model.to.assert_called_once_with("cpu")
        mock_assistant_model.to.assert_called_once_with("cpu")

    def test_get_parameters(self):
        """get_parametersメソッドのテスト"""
        # get_parametersメソッドを呼び出す
        parameters = self.gemma4_huggingface_response_generator.get_parameters()

        # 結果を検証
        assert isinstance(parameters, ChatModelParameter)
        assert parameters.temperature == 0.1
        assert parameters.thinking is None

    def test_update_parameters(self):
        """update_parametersメソッドのテスト"""
        # 新しいパラメータを作成
        new_parameters = ChatModelParameter(temperature=0.5, thinking=None)

        # update_parametersメソッドを呼び出す
        self.gemma4_huggingface_response_generator.update_parameters(new_parameters)

        # 結果を検証
        assert self.gemma4_huggingface_response_generator.temperature == 0.5

    @patch("modules.response_generator.gemma4_e2b.AutoProcessor")
    @patch("modules.response_generator.gemma4_e2b.AutoModelForCausalLM")
    def test_call(self, mock_auto_model_for_causal_lm, mock_auto_processor):
        """__call__メソッドのテスト"""
        # モックオブジェクトを設定
        mock_processor = MagicMock()
        mock_target_model = MagicMock()
        mock_assistant_model = MagicMock()
        mock_processor.apply_chat_template.return_value = "Hello"
        mock_inputs = MagicMock()
        mock_inputs_dict = {"input_ids": MagicMock()}
        mock_inputs.to.return_value = mock_inputs_dict
        mock_inputs_dict["input_ids"].shape = [1, 10]
        mock_processor.return_value = mock_inputs
        mock_target_model.generate.return_value = MagicMock()
        mock_processor.decode.return_value = "Hello, how can I help you?"
        mock_processor.parse_response.return_value = {
            "role": "assistant",
            "content": "Hello, how can I help you?",
        }
        self.gemma4_huggingface_response_generator.processor = mock_processor
        self.gemma4_huggingface_response_generator.target_model = mock_target_model
        self.gemma4_huggingface_response_generator.assistant_model = mock_assistant_model
        mock_target_model.device = "cuda"

        # 入力メッセージを作成
        input_messages = [ChatMessage(role="user", content="Hello")]

        # __call__メソッドを呼び出す
        response = self.gemma4_huggingface_response_generator(input_messages)

        # 結果を検証
        assert response == "Hello, how can I help you?"
