from enum import Enum

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
