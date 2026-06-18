import gc
import os
import time
from pathlib import Path

import torch
from langchain_community.chat_models import ChatLlamaCpp

from modules.logger import get_logger
from modules.schema import ChatMessage, ChatModel, ChatModelParameter

from .base import ResponseGenerator


class Gemma4LlmmaCppResponseGenerator(ResponseGenerator):
    """Gemma4:12Bを使用した返答生成クラス"""

    def __init__(self) -> None:
        """初期化"""
        super().__init__(
            logger=get_logger(__name__), name=ChatModel.GEMMA4_12B, is_use=torch.cuda.is_available()
        )
        self.data_dir = Path(os.getenv("DATA_DIR", "./develop"))

        self.target_model_id = self.data_dir.joinpath(
            "models", "gemma-4-12B-it-qat-q4_0-gguf", "gemma-4-12b-it-qat-q4_0.gguf"
        )
        self.max_tokens = 1024

        self.processor = None
        self.target_model = None

        # モデルのパラメータ
        self.temperature = 0.1

    def setup(self) -> None:
        """モデルのセットアップ"""
        self.llm = ChatLlamaCpp(
            model_path=str(self.target_model_id),
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            n_ctx=8192,
            n_gpu_layers=-1,
            n_batch=1024,
            verbose=True,
        )

        self.logger.info("モデルのセットアップが完了しました。")

    def cleanup(self) -> None:
        """モデル切り替え時にメモリを開放する"""
        # llama.cppの内部リソースを明示的に解放
        if self.llm is not None:
            if hasattr(self.llm, "client") and self.llm.client is not None:
                self.llm.client.close()
            del self.llm
            self.llm = None

        # ガベージコレクションを実行
        gc.collect()
        # CUDAキャッシュをクリア
        torch.cuda.empty_cache()

        self.logger.info("モデルのクリーンアップが完了しました。")

    def get_parameters(self) -> ChatModelParameter | None:
        """モデルのパラメータを取得する

        Returns:
            ChatModelParameter: モデルのパラメータのChatModelParameterオブジェクト
        """
        # モデルが使用可能な場合のみパラメータを返す
        if self.is_use:
            return ChatModelParameter(temperature=self.temperature, thinking=None)
        else:
            return None

    def update_parameters(self, parameters: ChatModelParameter) -> None:
        """モデルのパラメータを更新する

        Args:
            parameters (ChatModelParameter): 更新するパラメータを含むChatModelParameterオブジェクト
        """
        self.temperature = parameters.temperature

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
