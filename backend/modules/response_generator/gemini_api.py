import gc
import time

from langchain_google_genai import ChatGoogleGenerativeAI

from modules.logger import get_logger
from modules.schema import ChatMessage, ChatModel, ChatModelParameter, ResponseMetadata

from .base import ResponseGenerator


class GeminiResponseGenerator(ResponseGenerator):
    """Gemini APIを使用した返答生成クラス"""

    # 使用可能なモデルのリスト
    model_list = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
        "gemma-4-31b-it",
    ]

    def __init__(self) -> None:
        """初期化"""
        super().__init__(logger=get_logger(__name__), name=ChatModel.GEMINI, is_use=True)
        self.model_index = 0  # デフォルトのモデルインデックスを設定
        self.llm = None
        self.metadata = ResponseMetadata()

        # モデルのパラメータ
        self.temperature = 0.0
        self.thinking = "medium"
        self.thinking_budget_dict = {"low": 0, "medium": 1024, "high": 4096}

    def setup(self) -> None:
        """モデルのセットアップ"""
        self.model_name = self.model_list[self.model_index]
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

    def __call__(
        self, input_messages: list[dict[str, str]], user_message: ChatMessage
    ) -> tuple[str, ResponseMetadata]:
        """モデルの返答を生成する

        Args:
            input_messages (list[dict[str, str]]): これまでのチャット履歴
            user_message (ChatMessage): ユーザ入力文

        Returns:
            str: 生成された返答
        """
        start_time = time.perf_counter()

        # 入力データの変換
        formatted_messages = self.convert_input_messages(
            input_messages, user_message.content, num_ctx=5
        )

        last_exception: Exception | None = None
        for attempt in range(len(self.model_list)):
            try:
                if self.llm is None:
                    self.setup()

                # 返答の生成
                response = self.llm.invoke(formatted_messages)

                generate_time = time.perf_counter() - start_time
                self.logger.debug(f"返答の生成時間: {generate_time:.2f}s")

                # メタデータの取得
                self.metadata = self.create_metadata(response.response_metadata, generate_time)

                # テキストブロックのみを抽出する（thinking ブロックなどは除外される）
                raw_response = str(response.text)

                return raw_response, self.metadata

            except Exception as exception:
                last_exception = exception
                failed_model = self.model_list[self.model_index]
                self.cleanup()

                if attempt == len(self.model_list) - 1:
                    self.logger.error(
                        f"すべての Gemini モデルで返答生成に失敗しました。最後に失敗したモデル: "
                        f"'{failed_model}'",
                        exc_info=True,
                    )
                    break

                self.model_index = (self.model_index + 1) % len(self.model_list)
                next_model = self.model_list[self.model_index]
                self.logger.warning(
                    f"モデル '{failed_model}' で返答生成中にエラーが発生しました: {exception}。"
                    f"次のモデル '{next_model}' に切り替えてリトライします。"
                )

        assert last_exception is not None
        raise last_exception
