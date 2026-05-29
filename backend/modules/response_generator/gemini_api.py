import os
import time

from langchain_google_genai import ChatGoogleGenerativeAI

from modules.logger import get_logger
from modules.schema import ChatMessage, ChatModel


class GeminiResponseGenerator:
    """Gemini APIを使用した返答生成クラス"""

    def __init__(self) -> None:
        """初期化"""
        self.logger = get_logger(__name__)
        self.name = ChatModel.GEMINI

        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        self.llm = None

    def setup(self) -> None:
        """モデルのセットアップ"""
        self.llm = ChatGoogleGenerativeAI(model=self.model_name)

        self.logger.info("モデルのセットアップが完了しました。")

    def __call__(self, input_messages: list[ChatMessage]) -> str:
        """モデルの返答を生成する

        Args:
            input_messages (list[ChatMessage]): ユーザ入力を含むチャット履歴

        Returns:
            str: 生成された返答
        """
        # 返答の生成
        start_time = time.perf_counter()
        response = self.llm.invoke(input_messages)
        generate_time = time.perf_counter() - start_time
        self.logger.debug(f"返答の生成時間: {generate_time:.2f}s")

        # 生成された返答のデコード
        raw_response = response.content

        return raw_response
