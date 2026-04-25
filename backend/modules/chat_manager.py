import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from modules.schema import ChatMessage

# .envファイルから環境変数を読み込む
load_dotenv()


class ChatManager:
    """チャット履歴の管理と返答生成を行うクラス"""

    def __init__(self):
        self.data_dir = Path(os.getenv("DATA_DIR", "develop"))

        # チャット履歴の読み込み
        self.load_chat_history()

        # LLMの初期化
        self.llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    def load_chat_history(self) -> None:
        """チャット履歴の読み込み"""
        history_path = self.data_dir.joinpath("chat_history.json")
        if history_path.exists():
            with open(history_path, mode="r", encoding="utf-8") as f:
                self.chat_history = json.load(f)
        else:
            self.chat_history = []

    def save_chat_history(self) -> None:
        """チャット履歴の保存"""
        history_path = self.data_dir.joinpath("chat_history.json")
        with open(history_path, mode="w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, ensure_ascii=False, indent=4)

    def generate(self, user_message: ChatMessage) -> ChatMessage:
        """ユーザーからの入力に対してアシスタントの応答を生成する

        Args:
            user_message (ChatMessage): ユーザーからの入力メッセージ

        Returns:
            ChatMessage: アシスタントからの応答メッセージ
        """
        self.chat_history.append(user_message.model_dump())

        # LLMを使用して応答を生成
        response = self.llm.invoke(self.chat_history)

        # 生成された応答をChatMessage形式で返す
        assistant_message = ChatMessage(role="assistant", content=response.content)
        self.chat_history.append(assistant_message.model_dump())

        # チャット履歴を保存
        self.save_chat_history()

        return assistant_message
