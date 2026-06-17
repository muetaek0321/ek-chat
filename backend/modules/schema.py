from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, RootModel
from pydantic.alias_generators import to_camel


class Role(StrEnum):
    """チャットメッセージのroleを定義するEnum"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatModel(StrEnum):
    """使用するチャットモデルの名称を定義するEnum"""

    GEMINI = "Gemini(API)"
    GEMMA4_E2B = "Gemma4:E2B"
    GEMMA4_12B = "Gemma4:12B"


class Thinking(StrEnum):
    """思考時間の長さ設定名を定義Enum"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EndpointModel(BaseModel):
    """
    APIエンドポイントで使用する継承用BaseModel
    snake_case <-> camelCase の相互変換を設定
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ChatInfo(EndpointModel):
    """チャットの情報を表すBaseModel"""

    chat_id: str = Field(..., description="チャットID")
    title: str = Field(..., description="チャットのタイトル")


class ChatInfoList(RootModel[list[ChatInfo]]):
    """チャット一覧データのBaseModel"""

    root: list[ChatInfo] = Field(..., description="保存済みのチャット情報のリスト")


class SystemPromptText(EndpointModel):
    """SystemPromptのBaseModel"""

    text: str = Field(..., description="SystemPromptのテキスト")


class ChatModelParameter(EndpointModel):
    """チャットモデルのパラメータのBaseModel"""

    temperature: float | None = Field(
        ..., description="生成するテキストの多様性を制御するパラメータ"
    )
    thinking: Thinking | None = Field(
        ..., description="思考時間の長さを表すパラメータ（例: low, medium, high）"
    )


class SelectedChatModel(EndpointModel):
    """選択したチャットモデル情報のBaseModel"""

    model: ChatModel = Field(..., description="選択したチャットモデル")
    parameters: ChatModelParameter = Field(..., description="選択したチャットモデルのパラメータ")


class ChatModelInfo(EndpointModel):
    """チャットモデルの情報をまとめたBaseModel"""

    model_name: ChatModel = Field(..., description="チャットモデルの名称")
    is_use: bool = Field(..., description="チャットモデルが使用可能かどうか")
    is_selected: bool = Field(..., description="チャットモデルが選択されているかどうか")
    parameters: ChatModelParameter | None = Field(
        None, description="チャットモデルのパラメータ。モデルによってはNoneの可能性あり"
    )


class SettingsResponse(EndpointModel):
    """設定項目のResponseModel"""

    system_prompt: SystemPromptText = Field(..., description="SystemPrompt")
    chat_model_info_list: list[ChatModelInfo] = Field(..., description="チャットモデルの情報リスト")


class ChatMessage(EndpointModel):
    """チャットメッセージのBaseModel"""

    role: Role = Field(..., description="メッセージのrole（例: user, assistant）")
    content: str = Field(..., description="メッセージの内容")


class ChatHistory(RootModel[list[ChatMessage]]):
    """チャット履歴のBaseModel"""

    root: list[ChatMessage] = Field(..., description="チャットメッセージのリスト")


class ChatId(EndpointModel):
    """チャットIDのBaseModel"""

    chat_id: str | None = Field(None, description="チャットIDの指定")


class GenerateChatResponse(EndpointModel):
    """assistantの応答生成のResponseModel"""

    assistant_message: ChatMessage = Field(..., description="生成されたassistantのメッセージ")
    new_chat_info: ChatInfo | None = Field(
        None,
        description="新しいチャットが作成された場合のチャット情報。既存のチャットの保存の場合はNone",
    )
