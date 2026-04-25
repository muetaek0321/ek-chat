from pydantic import BaseModel, ConfigDict, Field, RootModel
from pydantic.alias_generators import to_camel


class EndpointModel(BaseModel):
    """
    APIエンドポイントで使用する継承用BaseModel
    snake_case <-> camelCase の相互変換を設定
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ChatMessage(EndpointModel):
    """チャットメッセージのモデル"""

    role: str = Field(..., description="メッセージのrole（例: user, assistant）")
    content: str = Field(..., description="メッセージの内容")


class ChatHistory(RootModel[list[ChatMessage]]):
    """チャット履歴のモデル"""

    root: list[ChatMessage] = Field(..., description="チャットメッセージのリスト")


class ChatRequest(EndpointModel):
    """チャットのリクエストモデル"""

    input_content: ChatMessage = Field(..., description="ユーザーからの入力内容")
    history: list[ChatMessage] = Field(..., description="チャット履歴")


class ChatResponse(EndpointModel):
    """チャットのレスポンスモデル"""

    response_content: ChatMessage = Field(..., description="アシスタントからの応答内容")
