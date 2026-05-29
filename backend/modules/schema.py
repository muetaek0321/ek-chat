from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, RootModel
from pydantic.alias_generators import to_camel


class Role(StrEnum):
    """チャットメッセージのroleを定義するEnum"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatModel(StrEnum):
    """使用するモデル"""

    GEMINI = "Gemini(API)"
    GEMMA4 = "Gemma4"


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
    """チャットの情報を表すモデル"""

    chat_id: str = Field(..., description="チャットID")
    title: str = Field(..., description="チャットのタイトル")


class ChatInfoList(RootModel[list[ChatInfo]]):
    """チャット一覧データのモデル"""

    root: list[ChatInfo] = Field(..., description="保存済みのチャット情報のリスト")


class SystemPromptText(EndpointModel):
    """SystemPromptのモデル"""

    text: str = Field(..., description="SystemPromptのテキスト")


class SelectedChatModel(EndpointModel):
    """選択したチャットモデル情報のモデル"""

    model: ChatModel = Field(..., description="選択したチャットモデル")


class ChatMessage(EndpointModel):
    """チャットメッセージのモデル"""

    role: Role = Field(..., description="メッセージのrole（例: user, assistant）")
    content: str = Field(..., description="メッセージの内容")


class ChatHistory(RootModel[list[ChatMessage]]):
    """チャット履歴のモデル"""

    root: list[ChatMessage] = Field(..., description="チャットメッセージのリスト")


class ChatId(EndpointModel):
    """チャットIDのモデル"""

    chat_id: str | None = Field(None, description="チャットIDの指定")


class GenerateChatResponse(EndpointModel):
    """assistantの応答生成のレスポンスモデル"""

    assistant_message: ChatMessage = Field(..., description="生成されたassistantのメッセージ")
    new_chat_info: ChatInfo | None = Field(
        None,
        description="新しいチャットが作成された場合のチャット情報。既存のチャットの保存の場合はNone",
    )
