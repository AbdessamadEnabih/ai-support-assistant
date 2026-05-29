from langfuse.openai import OpenAI
from langfuse import observe
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from enum import Enum
import json

load_dotenv()


from enum import Enum
from pydantic import BaseModel, Field


class CategoryEnum(str, Enum):
    billing = "billing"
    authentication = "authentication"
    bug_report = "bug_report"
    feature_request = "feature_request"
    account = "account"
    technical_issue = "technical_issue"
    general_inquiry = "general_inquiry"


class PriorityEnum(str, Enum):
    urgent = "urgent"
    high = "high"
    medium = "medium"
    low = "low"


class SentimentEnum(str, Enum):
    frustrated = "frustrated"
    neutral = "neutral"
    satisfied = "satisfied"
    confused = "confused"


# Optimized Schema for Local LLMs
class TicketClassification(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    sentiment: SentimentEnum
    summary: str = Field(description="One-sentence problem summary.")
    response_draft: str = Field(description="A short, max 2-sentence reply to the client.")


MODEL = "gemma-fast"

SYSTEM_PROMPT = "You are a precise support assistant backend. Your job is to categorize tickets into JSON format."

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

@observe()
def classify_ticket(prompt):
    completion = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format=TicketClassification,
        temperature=0.1,
        max_tokens=2000
    )

    response_text = completion.choices[0].message.content

    result = TicketClassification.model_validate_json(response_text)
    print(result)
    return result


if __name__ == "__main__":

    # example input : "I have an issue with my account, it keeps getting disbaled reguraly until i contact support can you fix the issue, this is very tiring"
    user_input = input("Whats the issue ?\n")
    classify_ticket(prompt=user_input)
