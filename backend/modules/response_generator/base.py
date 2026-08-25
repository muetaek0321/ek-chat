import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from modules.database.get_database_context import get_context
from modules.schema import ChatModel, ChatModelParameter, ResponseMetadata, Role


class ResponseGenerator(ABC):
    """返答生成クラスの継承元クラス"""

    def __init__(self, logger: logging.Logger, name: ChatModel, is_use: bool) -> None:
        """初期化

        Args:
            logger (logging.Logger): loggerオブジェクト
            name (ChatModel): モデルの名前
            is_use (bool): モデルを使用するかどうか
        """
        self.logger = logger
        self.name = name
        self.is_use = is_use
        self.model_name = ""
        self.metadata = ResponseMetadata()

    @abstractmethod
    def setup(self) -> None:
        """モデルのセットアップ"""
        raise NotImplementedError("setupメソッドは継承先で実装されていません")

    @abstractmethod
    def cleanup(self) -> None:
        """モデルのクリーンアップ"""
        raise NotImplementedError("cleanupメソッドは継承先で実装されていません")

    @abstractmethod
    def get_parameters(self) -> ChatModelParameter | None:
        """
        モデルのパラメータを取得する

        Returns:
            ChatModelParameter | None: モデルのパラメータのChatModelParameterオブジェクトまたはNone
        """
        raise NotImplementedError("get_parametersメソッドは継承先で実装されていません")

    @abstractmethod
    def update_parameters(self, parameters: ChatModelParameter) -> None:
        """
        モデルのパラメータを更新する

        Args:
            parameters (ChatModelParameter): 更新するパラメータを含むChatModelParameterオブジェクト
        """
        raise NotImplementedError("update_parametersメソッドは継承先で実装されていません")

    @abstractmethod
    def __call__(self, messages: list[dict[str, str]]) -> str:
        """
        返答を生成する

        Args:
            messages (list[dict[str, str]]): チャットメッセージのリスト

        Returns:
            str: 生成された返答
        """
        raise NotImplementedError("__call__メソッドは継承先で実装されていません")

    def convert_input_messages(
        self, input_messages: list[dict[str, str]], user_input: str, num_ctx: int = 5
    ) -> list[SystemMessage, HumanMessage, AIMessage]:
        """LLMに入力するメッセージのデータを変換

        Args:
            input_message (list[dict[str, str]]): 辞書型のメッセージデータ
            user_input (str): ユーザの入力文
            num_ctx (int): 検索で取得するコンテキスト数

        Returns:
            list[SystemMessage, HumanMessage, AIMessage]: LangChainのMessage形式に変換したデータ
        """
        converted_messages = []

        # チャット履歴のメッセージデータを変換
        for msg in input_messages:
            if msg["role"] == Role.SYSTEM:
                converted_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == Role.USER:
                converted_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == Role.ASSISTANT:
                converted_messages.append(AIMessage(content=msg["content"]))

        # 入力されたユーザに質問にはベクトルDBの検索結果を与えてRAGで回答させる
        converted_messages.append(HumanMessage(content=get_context(user_input, k=num_ctx)))

        return converted_messages

    def create_metadata(
        self, response_metadata: dict[Any], generate_time: float
    ) -> ResponseMetadata:
        """返答生成のメタデータを生成する

        Args:
            response_metadata (dict[Any]): 返答のメタ情報
            generate_time (float): 生成全体にかかった時間

        Returns:
            ResponseMetadata: 返答生成のメタ情報
        """
        # token/secの計算
        eval_count = response_metadata.get("eval_count")
        eval_duration = response_metadata.get("eval_duration")
        if eval_count is not None and eval_duration:
            tokens_per_second = round(eval_count / (eval_duration / 1_000_000_000), 2)
        else:
            tokens_per_second = None

        return ResponseMetadata(
            model_name=self.model_name,
            tokens_per_second=tokens_per_second,
            elapsed_time=round(generate_time, 2),
            executed_at=datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        )
