from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CamelBaseModel(BaseModel):
    """
    TypeScript(CamelCase) と Python(snake_case) の変換を
    自動で行うための共通ベースモデル
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True  # DBモデルなどから変換する場合にも便利
    )