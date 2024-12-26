from pydantic import BaseModel
from typing import Optional


class KanaResponse(BaseModel):
    text: str
    common: bool

class ExampleResponse(BaseModel):
    text: str
    sentence: str
    translation: str

class GlossResponse(BaseModel):
    lang: Optional[str]
    gender: Optional[str]
    type: Optional[str]
    text: str

class TagResponse(BaseModel):
    name: str
    definition: str