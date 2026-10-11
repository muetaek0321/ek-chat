from pydantic import BaseModel, ConfigDict
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
