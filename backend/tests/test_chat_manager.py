import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from dotenv import load_dotenv

from modules.chat_manager import ChatManager
from modules.schema import (
    ChatInfo,
    ChatInfoList,
    ChatMessage,
    ChatModel,
    ChatModelInfo,
    ChatModelParameter,
    GenerateChatResponse,
    Role,
    SystemPromptText,
    Thinking,
)

# 環境変数の読み込み
load_dotenv()


class TestChatManager:
    """ChatManagerクラスのテスト"""

    def setup_method(self):
        """テストメソッドのセットアップ"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)
        os.environ["DATA_DIR"] = str(self.data_dir)

        # chat_historyディレクトリを作成
        self.chat_history_dir = self.data_dir / "chat_history"
        self.chat_history_dir.mkdir(parents=True, exist_ok=True)

        # system_prompt.mdファイルを作成
        self.system_prompt_path = self.data_dir / "system_prompt.md"
        self.system_prompt_path.write_text("You are a helpful assistant.", encoding="utf-8")

        # ChatManagerのインスタンスを作成
        self.chat_manager = ChatManager()

    def teardown_method(self):
        """テストメソッドの teardown"""
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()

    def test_init(self):
        """__init__メソッドのテスト"""
        assert self.chat_manager.data_dir == self.data_dir
        assert self.chat_manager.current_chat_id == ""
        assert self.chat_manager.chat_history == []
        assert self.chat_manager.system_prompt is not None
        assert self.chat_manager.chat_model is not None

    def test_load_chat_list(self):
        """load_chat_listメソッドのテスト"""
        # テスト用のチャット履歴ファイルを作成
        chat_id = "20230101000000_1234567890"
        chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        chat_history_path = self.chat_history_dir / f"{chat_id}.json"
        with open(chat_history_path, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=4)

        # チャット一覧を読み込む
        chat_info_list = self.chat_manager.load_chat_list()

        # 結果を検証
        assert isinstance(chat_info_list, ChatInfoList)
        assert len(chat_info_list.root) == 1
        assert chat_info_list.root[0].chat_id == chat_id
        assert chat_info_list.root[0].title == "Hello"

    def test_new_chat(self):
        """new_chatメソッドのテスト"""
        # 新規チャットを作成
        new_chat_info = self.chat_manager.new_chat()

        # 結果を検証
        assert isinstance(new_chat_info, ChatInfo)
        assert new_chat_info.chat_id == "new"
        assert new_chat_info.title == "（新規チャット）"
        assert self.chat_manager.current_chat_id == "new"
        assert self.chat_manager.chat_history == []

    def test_delete_chat_new(self):
        """delete_chatメソッドのテスト (新規チャット)"""
        # 新規チャットを削除
        self.chat_manager.delete_chat("new")

        # 結果を検証 (特にエラーが発生しないことを確認)

    def test_delete_chat_existing(self):
        """delete_chatメソッドのテスト (既存チャット)"""
        # テスト用のチャット履歴ファイルを作成
        chat_id = "20230101000000_1234567890"
        chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        chat_history_path = self.chat_history_dir / f"{chat_id}.json"
        with open(chat_history_path, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=4)

        # チャットを削除
        self.chat_manager.delete_chat(chat_id)

        # 結果を検証
        assert not chat_history_path.exists()

    def test_load_chat_history_new(self):
        """load_chat_historyメソッドのテスト (新規チャット)"""
        # 新規チャットの履歴を読み込む
        chat_history = self.chat_manager.load_chat_history("new")

        # 結果を検証
        assert chat_history.root == []
        assert self.chat_manager.current_chat_id == "new"
        assert self.chat_manager.chat_history == []

    def test_load_chat_history_existing(self):
        """load_chat_historyメソッドのテスト (既存チャット)"""
        # テスト用のチャット履歴ファイルを作成
        chat_id = "20230101000000_1234567890"
        chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        chat_history_path = self.chat_history_dir / f"{chat_id}.json"
        with open(chat_history_path, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=4)

        # チャット履歴を読み込む
        loaded_chat_history = self.chat_manager.load_chat_history(chat_id)

        # 結果を検証
        assert len(loaded_chat_history.root) == 2
        assert loaded_chat_history.root[0].role == Role.USER
        assert loaded_chat_history.root[0].content == "Hello"
        assert loaded_chat_history.root[1].role == Role.ASSISTANT
        assert loaded_chat_history.root[1].content == "Hi"
        assert self.chat_manager.current_chat_id == chat_id

    def test_save_chat_history_new(self):
        """save_chat_historyメソッドのテスト (新規チャット)"""
        # 新規チャットの履歴を保存
        self.chat_manager.chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        new_chat_info = self.chat_manager.save_chat_history("new")

        # 結果を検証
        assert new_chat_info is not None
        assert isinstance(new_chat_info, ChatInfo)
        assert new_chat_info.title == "Hello"

        # 保存されたファイルを確認
        chat_history_files = list(self.chat_history_dir.glob("*.json"))
        assert len(chat_history_files) == 1
        saved_chat_id = chat_history_files[0].stem
        assert saved_chat_id != "new"
        with open(chat_history_files[0], "r", encoding="utf-8") as f:
            saved_chat_history = json.load(f)
        assert saved_chat_history == self.chat_manager.chat_history

    def test_save_chat_history_existing(self):
        """save_chat_historyメソッドのテスト (既存チャット)"""
        # テスト用のチャット履歴ファイルを作成
        chat_id = "20230101000000_1234567890"
        chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        chat_history_path = self.chat_history_dir / f"{chat_id}.json"
        with open(chat_history_path, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=4)

        # 既存チャットの履歴を更新
        self.chat_manager.current_chat_id = chat_id
        self.chat_manager.chat_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm fine, thank you."},
        ]
        new_chat_info = self.chat_manager.save_chat_history(chat_id)

        # 結果を検証
        assert new_chat_info is None
        with open(chat_history_path, "r", encoding="utf-8") as f:
            saved_chat_history = json.load(f)
        assert saved_chat_history == self.chat_manager.chat_history

    def test_load_system_prompt(self):
        """load_system_promptメソッドのテスト"""
        # SystemPromptを読み込む
        self.chat_manager.load_system_prompt()

        # 結果を検証
        assert self.chat_manager.system_prompt is not None
        assert self.chat_manager.system_prompt.content == "You are a helpful assistant."

    def test_get_system_prompt(self):
        """get_system_promptメソッドのテスト"""
        # SystemPromptを取得
        system_prompt_text = self.chat_manager.get_system_prompt()

        # 結果を検証
        assert isinstance(system_prompt_text, SystemPromptText)
        assert system_prompt_text.text == "You are a helpful assistant."

    def test_update_system_prompt(self):
        """update_system_promptメソッドのテスト"""
        # 新しいSystemPromptを設定
        new_system_prompt = "You are a helpful assistant. Please be polite."
        self.chat_manager.update_system_prompt(new_system_prompt)

        # 結果を検証
        assert self.chat_manager.system_prompt.content == new_system_prompt
        with open(self.system_prompt_path, "r", encoding="utf-8") as f:
            saved_system_prompt = f.read()
        assert saved_system_prompt == new_system_prompt

    def test_get_chat_model_info(self):
        """get_chat_model_infoメソッドのテスト"""
        # チャットモデル一覧を取得
        chat_model_info_list = self.chat_manager.get_chat_model_info()

        # 結果を検証
        assert isinstance(chat_model_info_list, list)
        assert len(chat_model_info_list) == 4
        for chat_model_info in chat_model_info_list:
            assert isinstance(chat_model_info, ChatModelInfo)
            assert chat_model_info.model_name in ChatModel
            assert isinstance(chat_model_info.is_use, bool)
            assert isinstance(chat_model_info.is_selected, bool)
            if chat_model_info.parameters is not None:
                assert isinstance(chat_model_info.parameters, ChatModelParameter)

    def test_change_chat_model(self):
        """change_chat_modelメソッドのテスト"""
        # モックオブジェクトを作成
        mock_old_model = MagicMock()
        self.chat_manager.chat_model = mock_old_model
        mock_new_model = MagicMock()
        self.chat_manager.chat_models[ChatModel.GEMMA4_E2B] = mock_new_model

        # チャットモデルを変更
        parameters = ChatModelParameter(temperature=0.5, thinking=Thinking.MEDIUM)
        self.chat_manager.change_chat_model(ChatModel.GEMMA4_E2B, parameters)

        # 結果を検証
        assert self.chat_manager.chat_model == mock_new_model
        mock_old_model.cleanup.assert_called_once()
        mock_new_model.update_parameters.assert_called_once_with(parameters)
        mock_new_model.setup.assert_called_once()

    def test_generate(self):
        """generateメソッドのテスト"""
        # モックオブジェクトを設定
        mock_response = "Hello, how can I help you?"
        self.chat_manager.chat_model = MagicMock()
        self.chat_manager.chat_model.return_value = mock_response

        # 事前に新規チャット作成
        self.chat_manager.new_chat()

        # ユーザーメッセージを作成
        user_message = ChatMessage(role=Role.USER, content="Hello")

        # 応答を生成
        generate_chat_response = self.chat_manager.generate(user_message)

        # 結果を検証
        assert isinstance(generate_chat_response, GenerateChatResponse)
        assert generate_chat_response.assistant_message.role == Role.ASSISTANT
        assert generate_chat_response.assistant_message.content == mock_response
        assert generate_chat_response.new_chat_info is not None
        assert isinstance(generate_chat_response.new_chat_info, ChatInfo)
