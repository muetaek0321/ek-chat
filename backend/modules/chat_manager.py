import json
import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from modules.logger import get_logger
from modules.response_generator.gemini_api import GeminiResponseGenerator
from modules.response_generator.gemma4_12b import Gemma4LlmmaCppResponseGenerator
from modules.response_generator.gemma4_e2b import Gemma4HuggingFaceResponseGenerator
from modules.response_generator.muse_glimmer import MuseGlimmerResponseGenerator
from modules.response_generator.ollama_cloud import OllamaCloudResponseGenerator
from modules.response_generator.qwen import QwenResponseGenerator
from modules.schema import (
    ChatHistory,
    ChatInfo,
    ChatInfoList,
    ChatMessage,
    ChatModel,
    ChatModelInfo,
    ChatModelParameter,
    GenerateChatResponse,
    Role,
    SystemPromptText,
)

# ロガーのインスタンスを取得
logger = get_logger(__name__)


class ChatManager:
    """チャット履歴の管理と返答生成を行うクラス"""

    def __init__(self):
        self.data_dir = Path(os.getenv("DATA_DIR", "./develop"))

        self.current_chat_id = ""
        self.chat_history = []

        # SystemPromptの読み込み
        self.load_system_prompt()

        # 使用可能なモデル一覧（GPUが使用可能かどうかで動的に変更）
        self.chat_models = {
            ChatModel.GEMINI: GeminiResponseGenerator(),
            ChatModel.GEMMA4_E2B: Gemma4HuggingFaceResponseGenerator(),
            ChatModel.GEMMA4_12B: Gemma4LlmmaCppResponseGenerator(),
            ChatModel.QWEN: QwenResponseGenerator(),
            ChatModel.MUSE_GLIMMER: MuseGlimmerResponseGenerator(),
            ChatModel.OLLAMA_CLOUD: OllamaCloudResponseGenerator(),
        }

        # 使用するモデルの初期化
        self.chat_model = self.chat_models[os.getenv("CHAT_MODEL", ChatModel.GEMINI)]
        self.chat_model.setup()

    def load_chat_list(self) -> ChatInfoList:
        """保存済みのチャット一覧の情報を読み込み

        Returns:
            ChatInfoList: 保存済みチャット一覧のデータ
        """
        chat_info_list = []
        chat_history_dir = self.data_dir.joinpath("chat_history")

        # 保存先フォルダ内のチャット履歴ファイルを確認し、IDのリストを作成
        chat_ids = [f.stem for f in chat_history_dir.glob("*.json")]
        # チャット履歴の読み込んでチャット情報のリストを作成
        for chat_id in chat_ids:
            chat_history = self.load_chat_history(chat_id=chat_id)
            # 最初のユーザ入力の内容をタイトルにする
            title = chat_history.root[0].content[:15]
            chat_info_list.append(ChatInfo(chat_id=chat_id, title=title))

        return ChatInfoList(chat_info_list)

    def new_chat(self) -> ChatInfo:
        """新規チャットの作成

        Returns:
            ChatInfo: 新しいチャットの情報データ
        """
        # 未設定のチャットID
        new_chat_id = "new"

        # 新しいチャットを作成するためのデータを設定
        new_chat_info = ChatInfo(chat_id=new_chat_id, title="（新規チャット）")
        self.current_chat_id = new_chat_id
        self.chat_history = []

        return new_chat_info

    def delete_chat(self, chat_id: str) -> None:
        """チャットの削除

        Args:
            chat_id (str): 削除するチャットのID
        """
        if chat_id == "new":
            # NOTE: 新規チャットの時点では履歴ファイルが存在しないため
            logger.info("新規チャットの削除のためスキップ")
        else:
            # 指定IDのチャット履歴ファイルを削除
            history_path = self.data_dir.joinpath("chat_history", f"{chat_id}.json")
            history_path.unlink()

    def load_chat_history(self, chat_id: str) -> ChatHistory:
        """チャット履歴の読み込み

        Args:
            chat_id (str): 読み込むチャットのID

        Returns:
            ChatHistory: 読み込んだチャット履歴データ
        """
        # 新規チャットの指定の場合
        if chat_id == "new":
            self.chat_history = []
        else:
            history_path = self.data_dir.joinpath("chat_history", f"{chat_id}.json")
            if history_path.exists():
                with open(history_path, mode="r", encoding="utf-8") as f:
                    self.chat_history = json.load(f)
            else:
                raise FileNotFoundError(f"指定のIDのチャット履歴が見つかりません: {chat_id}")

        # 指定のチャットIDを選択中のチャットIDに設定
        self.current_chat_id = chat_id

        return ChatHistory(self.chat_history)

    def save_chat_history(self, chat_id: str) -> ChatInfo | None:
        """チャット履歴の保存

        Args:
            chat_id (str): 保存するチャットのID

        Returns:
            ChatInfo | None: 新しいチャットが作成された場合はそのチャット情報、既存のチャットの保存の場合はNone
        """
        # 新しいチャットからの作成の場合
        if chat_id == "new":
            # チャットIDが未設定の場合は新しいIDを生成
            chat_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4()}"
            # タイトルの作成
            title = ChatHistory(self.chat_history).root[0].content[:15]
            # 新しいチャットのチャット情報の作成
            new_chat_info = ChatInfo(chat_id=chat_id, title=title)
        else:
            new_chat_info = None

        # チャット履歴をjsonファイルで保存
        history_path = self.data_dir.joinpath("chat_history", f"{chat_id}.json")
        with open(history_path, mode="w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, ensure_ascii=False, indent=4)

        return new_chat_info

    def load_system_prompt(self) -> None:
        """SystemPromptの読み込み"""
        system_prompt_path = self.data_dir.joinpath("system_prompt.md")

        if system_prompt_path.exists():
            with open(system_prompt_path, mode="r", encoding="utf-8") as f:
                self.system_prompt = ChatMessage(role="system", content=f.read())
                logger.info("SystemPromptを読み込みました。")
        else:
            self.system_prompt = None
            logger.warning("SystemPromptのファイルが見つかりません。")

    def get_system_prompt(self) -> SystemPromptText:
        """SystemPromptを取得"""
        system_prompt_text = self.system_prompt.content if self.system_prompt is not None else ""
        return SystemPromptText(text=system_prompt_text)

    def update_system_prompt(self, system_prompt_text: str) -> None:
        """SystemPromptを作成/更新し登録

        Args:
            system_prompt_text: SystemPromptのテキスト
        """
        # ファイルを作成/更新
        system_prompt_path = self.data_dir.joinpath("system_prompt.md")
        with open(system_prompt_path, mode="w", encoding="utf-8") as f:
            f.write(system_prompt_text)

        # 登録中のSystemPromptの更新
        self.system_prompt = ChatMessage(role=Role.SYSTEM, content=system_prompt_text)

    def get_chat_model_info(self) -> list[ChatModelInfo]:
        """チャットモデル一覧の情報を取得"""
        chat_model_info_list = []

        # チャットモデルの情報を取得
        for model_name, model in self.chat_models.items():
            chat_model_info_list.append(
                ChatModelInfo(
                    model_name=model_name,
                    is_use=model.is_use,
                    is_selected=model_name == self.chat_model.name,
                    parameters=model.get_parameters(),
                )
            )

        return chat_model_info_list

    def change_chat_model(self, chat_model_name: ChatModel, parameters: ChatModelParameter) -> None:
        """選択されたチャットモデルに変更し設定を適用

        Args:
            chat_model_name (ChatModel): 変更するチャットモデル
            parameters (ChatModelParameter): チャットモデルのパラメータ
        """
        # 現在使用中のモデルのGPUメモリを解放
        if self.chat_model is not None:
            self.chat_model.cleanup()

        # 使用するモデルを変更
        self.chat_model = self.chat_models[chat_model_name.value]
        # モデルのパラメータを更新
        self.chat_model.update_parameters(parameters)

        # モデルの初期化
        self.chat_model.setup()

    def generate(self, user_message: ChatMessage) -> GenerateChatResponse:
        """ユーザーからの入力に対してアシスタントの応答を生成する

        Args:
            user_message (ChatMessage): ユーザーからの入力メッセージ

        Returns:
            GenerateChatResponse: アシスタントからの応答メッセージと新しいチャット情報
        """
        input_messages = self.chat_history.copy()

        # SystemPromptが設定されている場合はチャット履歴の先頭にSystemPromptを追加
        if self.system_prompt:
            logger.debug("SystemPromptを利用します。")
            input_messages.insert(0, self.system_prompt.model_dump())

        # LLMを使用して応答を生成
        response, metadata = self.chat_model(input_messages, user_message)

        # 生成された応答をChatMessage形式で返す
        assistant_message = ChatMessage(role=Role.ASSISTANT, content=response, metadata=metadata)
        # ユーザ入力と返答文を履歴に追加
        self.chat_history.append(user_message.model_dump())
        self.chat_history.append(assistant_message.model_dump())

        # チャット履歴を保存
        new_chat_info = self.save_chat_history(chat_id=self.current_chat_id)

        return GenerateChatResponse(
            assistant_message=assistant_message, new_chat_info=new_chat_info
        )
