from pydantic import BaseModel


class SubtitleDTO(BaseModel):
    start: str
    end: str
    text: str


class SummaryDTO(BaseModel):
    summary: str
