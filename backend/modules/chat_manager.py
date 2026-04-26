import json
import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from modules.schema import ChatHistory, ChatMessage

# .envファイルから環境変数を読み込む
load_dotenv()


class ChatManager:
    """チャット履歴の管理と返答生成を行うクラス"""

    def __init__(self):
        self.data_dir = Path(os.getenv("DATA_DIR", "develop"))

        self.chat_ids = []
        self.current_chat_id = None
        self.chat_history = []

        # 保存済みのチャット履歴の読み込み
        self.load_chat_list()

        # LLMの初期化
        self.llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    def load_chat_list(self) -> None:
        """保存済みのチャット一覧の情報を読み込み"""
        chat_history_dir = self.data_dir.joinpath("chat_history")

        # 保存先フォルダ内のチャット履歴ファイルを確認し、IDのリストを作成
        self.chat_ids = [f.stem for f in chat_history_dir.glob("*.json")]
        if len(self.chat_ids) == 0:
            # チャット履歴が存在しない場合は新規チャットを作成
            self.new_chat()
        else:
            self.current_chat_id = self.chat_ids[-1]

        # チャット履歴の読み込み
        self.load_chat_history(chat_id=self.current_chat_id)

    def new_chat(self) -> str:
        """新規チャットの作成"""
        # チャットIDを生成
        new_chat_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4()}"

        # チャットIDを管理リストに追加
        self.chat_ids.append(new_chat_id)
        self.current_chat_id = new_chat_id
        # チャット履歴を初期化
        self.chat_history = []

        # チャット履歴ファイルの新規作成
        self.save_chat_history(chat_id=new_chat_id)

        return new_chat_id

    def load_chat_history(self, chat_id: str | None = None) -> ChatHistory:
        """チャット履歴の読み込み

        Args:
            chat_id (str | None): 読み込むチャットのID。Noneの場合は選択中のチャットIDを使用
        """
        # チャットIDが指定されていない場合はリストの選択中のチャットIDを使用
        if chat_id is None:
            chat_id = self.current_chat_id

        history_path = self.data_dir.joinpath("chat_history", f"{chat_id}.json")
        if history_path.exists():
            with open(history_path, mode="r", encoding="utf-8") as f:
                self.chat_history = json.load(f)
        else:
            raise FileNotFoundError(f"指定のIDのチャット履歴が見つかりません: {chat_id}")

        # 指定のチャットIDを選択中のチャットIDに設定
        self.current_chat_id = chat_id

        return ChatHistory(self.chat_history)

    def save_chat_history(self, chat_id: str) -> None:
        """チャット履歴の保存

        Args:
            chat_id (str): 保存するチャットのID
        """
        history_path = self.data_dir.joinpath("chat_history", f"{chat_id}.json")
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
        self.save_chat_history(chat_id=self.current_chat_id)

        return assistant_message
