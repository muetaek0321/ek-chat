import logging
from abc import ABC, abstractmethod

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from modules.database.get_database_context import get_context
from modules.schema import ChatModel, ChatModelParameter, Role


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
        self, input_messages: list[dict[str, str]], user_input: str
    ) -> list[SystemMessage, HumanMessage, AIMessage]:
        """LLMに入力するメッセージのデータを変換

        Args:
            input_message (list[dict[str, str]]): 辞書型のメッセージデータ
            user_input (str): ユーザの入力文

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
        converted_messages.append(HumanMessage(content=get_context(user_input)))

        return converted_messages
