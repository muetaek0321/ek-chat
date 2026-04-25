import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from modules.schema import ChatMessage

# .envファイルから環境変数を読み込む
load_dotenv()


class ChatManager:
    """チャット履歴の管理と返答生成を行うクラス"""

    def __init__(self):
        self.chat_history = []
        self.llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    def generate(self, user_message: dict[str, str] | ChatMessage) -> ChatMessage:
        """ユーザーからの入力に対してアシスタントの応答を生成する

        Args:
            user_message (dict[str, str] | ChatMessage): ユーザーからの入力メッセージ

        Returns:
            ChatMessage: アシスタントからの応答メッセージ
        """
        self.chat_history.append(user_message)

        # LLMを使用して応答を生成
        response = self.llm.invoke(self.chat_history)

        # 生成された応答をChatMessage形式で返す
        assistant_message = ChatMessage(role="assistant", content=response.content)
        self.chat_history.append(assistant_message)

        return assistant_message
