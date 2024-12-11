from pydantic import BaseModel


class GetQuestion(BaseModel):
    category: str