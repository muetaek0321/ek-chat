import gc
import os
import time

from langchain_google_genai import ChatGoogleGenerativeAI

from modules.logger import get_logger
from modules.schema import ChatMessage, ChatModel, ChatModelParameter, ResponseMetadata

from .base import ResponseGenerator


class GeminiResponseGenerator(ResponseGenerator):
    """Gemini APIを使用した返答生成クラス"""

    def __init__(self) -> None:
        """初期化"""
        super().__init__(logger=get_logger(__name__), name=ChatModel.GEMINI, is_use=True)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
        self.llm = None
        self.metadata = ResponseMetadata()

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

    def cleanup(self) -> None:
        """モデル切り替え時にメモリを開放する"""
        # モデルオブジェクトを削除して変数を初期化
        del self.llm
        self.llm = None

        # ガベージコレクションを実行
        gc.collect()

        self.logger.info("モデルのクリーンアップが完了しました。")

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

    def __call__(self, input_messages: list[dict[str, str]], user_message: ChatMessage) -> str:
        """モデルの返答を生成する

        Args:
            input_messages (list[dict[str, str]]): これまでのチャット履歴
            user_message (ChatMessage): ユーザ入力文

        Returns:
            str: 生成された返答
        """
        start_time = time.perf_counter()

        # 入力データの変換
        input_messages = self.convert_input_messages(
            input_messages, user_message.content, num_ctx=5
        )

        # 返答の生成
        response = self.llm.invoke(input_messages)

        generate_time = time.perf_counter() - start_time
        self.logger.debug(f"返答の生成時間: {generate_time:.2f}s")

        # メタデータの取得
        self.metadata = self.create_metadata(response.response_metadata, generate_time)

        # 生成された返答のデコード
        raw_response = response.content[0]["text"]

        return raw_response, self.metadata
