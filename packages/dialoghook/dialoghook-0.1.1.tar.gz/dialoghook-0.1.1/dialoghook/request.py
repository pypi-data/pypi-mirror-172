from typing import Any, List, Dict
from enum import Enum

from .common import Message, Context

from pydantic import BaseModel


class WebhookState(Enum):
    WEBHOOK_STATE_UNSPECIFIED = "WEBHOOK_STATE_UNSPECIFIED"
    WEBHOOK_STATE_ENABLED = "WEBHOOK_STATE_ENABLED"
    WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING = "WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING"


class Type(Enum):
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    EXAMPLE = "EXAMPLE"


class Part(BaseModel):
    text: str
    entityType: str | None
    alias: str | None
    userDefined: bool | None


class TrainingPhrase(BaseModel):
    name: str
    type: Type
    parts: List[Part]
    timesAddedCount: int | None


class FollowupIntentInfo(BaseModel):
    followupIntentName: str
    parentFollowupIntentName: str


class Intent(BaseModel):
    displayName: str
    name: str | None
    webhookState: WebhookState | None
    priority: int | None
    isFallback: bool | None
    mlDisabled: bool | None
    liveAgentHandoff: bool | None
    endInteraction: bool | None
    inputContextNames: List[str] | None
    events: List[str] | None
    trainingPhrases: List[TrainingPhrase] | None
    action: str | None
    outputContexts: List[Context] | None
    resetContexts: bool | None
    # https://cloud.google.com/dialogflow/es/docs/reference/rest/v2/projects.agent.intents#Intent.Parameter
    parameters: List[dict] | None
    messages: List[Message] | None
    defaultResponsePlatforms: List[Any] | None
    rootFollowupIntentName: str | None
    parentFollowupIntentName: str | None
    followupIntentInfo: List[FollowupIntentInfo] | None

    class Config:
        use_enum_values = True


class Sentiment(BaseModel):
    score: int
    magnitude: int


class SentimentAnalysisResult(BaseModel):
    queryTextSentiment: Sentiment


class QueryResult(BaseModel):
    """https://cloud.google.com/dialogflow/es/docs/reference/rest/v2/DetectIntentResponse#QueryResult"""
    queryText: str
    # language enum here, https://cloud.google.com/dialogflow/es/docs/reference/language
    languageCode: str
    speechRecognitionConfidence: int | None
    action: str | None
    parameters: Dict[str, dict | str | int | bool | list] | None
    allRequiredParamsPresent: bool
    cancelsSlotFilling: bool | None
    fulfillmentText: str | None
    fulfillmentMessages: List[Message] | None
    webhookSource: str | None
    webhookPayload: dict | None
    outputContexts: List[Context] | None
    intent: Intent
    intentDetectionConfidence: int
    diagnosticInfo: dict
    sentimentAnalysisResult: SentimentAnalysisResult | None

class OriginalDetectIntentRequest(BaseModel):
    source: str | None
    version: str | None
    payload: Dict[str, dict] | None

class WebhookRequest(BaseModel):
    """
    """
    session: str
    responseId: str
    queryResult: QueryResult
    originalDetectIntentRequest: OriginalDetectIntentRequest | None


request = WebhookRequest.parse_file("tests\\request-01.json")

print(request)

