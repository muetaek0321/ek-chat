import json
import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from modules.schema import ChatHistory, ChatInfo, ChatInfoList, ChatMessage

# .envファイルから環境変数を読み込む
load_dotenv()


class ChatManager:
    """チャット履歴の管理と返答生成を行うクラス"""

    def __init__(self):
        self.data_dir = Path(os.getenv("DATA_DIR", "./develop"))

        self.chat_info_list = []
        self.current_chat_id = None
        self.chat_history = []

        # 保存済みのチャット履歴の読み込み
        self.load_chat_list()

        # LLMの初期化
        self.llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    def load_chat_list(self) -> ChatInfoList:
        """保存済みのチャット一覧の情報を読み込み"""
        self.chat_info_list = []
        chat_history_dir = self.data_dir.joinpath("chat_history")

        # 保存先フォルダ内のチャット履歴ファイルを確認し、IDのリストを作成
        chat_ids = [f.stem for f in chat_history_dir.glob("*.json")]
        if len(chat_ids) == 0:
            # チャット履歴が存在しない場合は新規チャットを作成
            self.new_chat()
        else:
            # チャット履歴の読み込んでチャット情報のリストを作成
            for chat_id in chat_ids:
                chat_history = self.load_chat_history(chat_id=chat_id)
                # 最初のユーザ入力の内容をタイトルにする
                title = chat_history.root[0].content[:15]
                self.chat_info_list.append(ChatInfo(chat_id=chat_id, title=title))

        return ChatInfoList(self.chat_info_list)

    def new_chat(self) -> str:
        """新規チャットの作成"""
        # チャットIDを生成
        new_chat_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4()}"

        # チャットIDを管理リストに追加
        self.chat_info_list.append(ChatInfo(chat_id=new_chat_id, title="新規チャット"))
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
