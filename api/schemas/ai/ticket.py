from pydantic import BaseModel, Field
from ..enum import CategoryEnum, PriorityEnum, SentimentEnum


class Ticket(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    sentiment: SentimentEnum
    summary: str = Field(description="One-sentence problem summary.")
    response_draft: str = Field(
        description="A short, max 2-sentence reply to the client."
    )
