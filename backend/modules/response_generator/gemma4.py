import os
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoProcessor

from modules.logger import get_logger
from modules.schema import ChatMessage, ChatModel, ChatModelParameter


class Gemma4ResponseGenerator:
    """Gemma4:E2Bを使用した返答生成クラス"""

    def __init__(self) -> None:
        """初期化"""
        self.data_dir = Path(os.getenv("DATA_DIR", "./develop"))
        self.logger = get_logger(__name__)
        self.name = ChatModel.GEMMA4
        self.is_use = torch.cuda.is_available()  # GPUが使用可能な場合のみ使用可能

        self.target_model_id = self.data_dir.joinpath("models", "gemma-4-E2B-it")
        self.assistant_model_id = self.data_dir.joinpath("models", "gemma-4-E2B-it-assistant")
        self.max_new_tokens = 512

        self.processor = None
        self.target_model = None
        self.assistant_model = None

    def setup(self) -> None:
        """モデルのセットアップ"""
        # 対象モデル
        self.processor = AutoProcessor.from_pretrained(self.target_model_id)
        self.target_model = AutoModelForCausalLM.from_pretrained(
            self.target_model_id,
            dtype="auto",
            device_map="auto",
        )

        # 補助モデル
        self.assistant_model = AutoModelForCausalLM.from_pretrained(
            self.assistant_model_id,
            dtype="auto",
            device_map="auto",
        )

        self.logger.info("モデルのセットアップが完了しました。")

    def get_parameters(self) -> ChatModelParameter | None:
        """モデルのパラメータを取得する

        Returns:
            ChatModelParameter: モデルのパラメータのChatModelParameterオブジェクト
        """
        # モデルが使用可能な場合のみパラメータを返す
        if self.is_use:
            return None  # TODO: Gemma4のパラメータを調査してから設定
        else:
            return None

    def update_parameters(self, parameters: ChatModelParameter) -> None:
        """モデルのパラメータを更新する

        Args:
            parameters (ChatModelParameter): 更新するパラメータを含むChatModelParameterオブジェクト
        """
        raise NotImplementedError("Gemma4のパラメータ更新は未実装です。")

    def __call__(self, input_messages: list[ChatMessage]) -> str:
        """モデルの返答を生成する

        Args:
            input_messages (list[ChatMessage]): ユーザ入力を含むチャット履歴

        Returns:
            str: 生成された返答
        """
        # チャットテンプレートの設定
        text = self.processor.apply_chat_template(
            input_messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        # 入力データの処理
        inputs = self.processor(text=text, return_tensors="pt").to(self.target_model.device)
        input_len = inputs["input_ids"].shape[-1]

        # 返答の生成
        start_time = time.perf_counter()
        outputs = self.target_model.generate(
            **inputs,
            assistant_model=self.assistant_model,
            max_new_tokens=self.max_new_tokens,
        )
        generate_time = time.perf_counter() - start_time
        self.logger.debug(f"返答の生成時間: {generate_time:.2f}s")

        # 生成された返答のデコード
        raw_response = self.processor.decode(outputs[0][input_len:], skip_special_tokens=False)

        # 返答をパースしてcontentのみを取得
        response = self.processor.parse_response(raw_response)["content"]

        return response
