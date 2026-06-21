import gc
import os
import time

from langchain_ollama import ChatOllama

from modules.logger import get_logger
from modules.schema import ChatMessage, ChatModel, ChatModelParameter

from .base import ResponseGenerator


class OllamaCloudResponseGenerator(ResponseGenerator):
    """OllamaCloudを使用した返答生成クラス"""

    def __init__(self) -> None:
        """初期化"""
        super().__init__(logger=get_logger(__name__), name=ChatModel.OLLAMA, is_use=True)
        self.model_name = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
        self.llm = None

        # モデルのパラメータ
        self.temperature = 0.1
        self.thinking = "medium"

    def setup(self) -> None:
        """モデルのセットアップ"""
        self.llm = ChatOllama(
            model=self.model_name,
            base_url="https://ollama.com",
            api_key=os.getenv("OLLAMA_API_KEY", None),
            temperature=self.temperature,
            reasoning_effort=self.thinking,
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
