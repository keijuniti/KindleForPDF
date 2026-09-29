from pydantic import Field
from src.domain.models.utils.accept_camel import CamelBaseModel

class CaptureConfig(CamelBaseModel):
    page_count: int = Field(gt=0)
    interval: float = Field(ge=0)
    output_filename: str = Field(min_length=1)
    use_grayscale: bool = False
    resize_factor: float = Field(default=1.0, gt=0, le=1)
    target_window_title: str
