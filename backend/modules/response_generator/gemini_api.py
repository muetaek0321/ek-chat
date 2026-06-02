import os
import time

from langchain_google_genai import ChatGoogleGenerativeAI

from modules.logger import get_logger
from modules.schema import ChatMessage, ChatModel, ChatModelParameter


class GeminiResponseGenerator:
    """Gemini APIを使用した返答生成クラス"""

    def __init__(self) -> None:
        """初期化"""
        self.logger = get_logger(__name__)
        self.name = ChatModel.GEMINI
        self.is_use = True

        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

        self.llm = None

        # モデルのパラメータ
        self.temperature = 0.0
        self.thinking = "medium"
        self.thinking_budget_dict = {"low": 0, "medium": 1024, "high": 4096}

    def setup(self) -> None:
        """モデルのセットアップ"""
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            thinking_budget=self.thinking_budget_dict[self.thinking],
        )

        self.logger.info("モデルのセットアップが完了しました。")

    def get_parameters(self) -> ChatModelParameter | None:
        """モデルのパラメータを取得する

        Returns:
            ChatModelParameter: モデルのパラメータのChatModelParameterオブジェクト
        """
        # モデルが使用可能な場合のみパラメータを返す
        if self.is_use:
            return ChatModelParameter(temperature=self.temperature, thinking=self.thinking)
        else:
            return None

    def update_parameters(self, parameters: ChatModelParameter) -> None:
        """モデルのパラメータを更新する

        Args:
            parameters (ChatModelParameter): 更新するパラメータを含むChatModelParameterオブジェクト
        """
        self.temperature = parameters.temperature
        self.thinking = parameters.thinking

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
