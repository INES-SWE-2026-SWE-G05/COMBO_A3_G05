from typing import Any

from pydantic import BaseModel, Field, field_validator

from .settings import MAX_QUESTION_LENGTH


class AskRequest(BaseModel):
    question: str = Field(max_length=MAX_QUESTION_LENGTH)

    @field_validator("question")
    @classmethod
    def question_must_have_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Question must not be blank")
        return cleaned


class AskResponse(BaseModel):
    query: str
    match: dict[str, Any] | None
    confidence: float
    reason: str
    introduction: str | None
    evidenceLinks: list[str]
    modelVersion: str
    groupCode: str
    source: str

