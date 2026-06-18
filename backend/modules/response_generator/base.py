import logging
from abc import ABC, abstractmethod

from modules.schema import ChatModel, ChatModelParameter


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
