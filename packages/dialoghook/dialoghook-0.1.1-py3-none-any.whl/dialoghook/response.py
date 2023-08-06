from typing import List, Dict
from enum import Enum

from .common import Message, Context

from pydantic import BaseModel

class EntityOverrideMode(Enum):
    ENTITY_OVERRIDE_MODE_UNSPECIFIED= "ENTITY_OVERRIDE_MODE_UNSPECIFIED"
    ENTITY_OVERRIDE_MODE_OVERRIDE = "ENTITY_OVERRIDE_MODE_OVERRIDE"
    ENTITY_OVERRIDE_MODE_SUPPLEMENT = "ENTITY_OVERRIDE_MODE_SUPPLEMENT"

class EventInput(BaseModel):
    name: str | None
    parameters: Dict[str, str |int |bool | list | dict] | None
    languageCode: str | None

class Entity(BaseModel):
    value: str
    synonyms: List[str]

class SessionEntityType(BaseModel):
    name: str
    entityOverrideMode: EntityOverrideMode
    entities: Entity

class WebhookResponse(BaseModel):
    fulfillmentText: str | None
    fulfillmentMessages: List[Message] | None
    source: str | None
    payload: dict | None
    outputContext: List[Context] | None
    followupEventInput: EventInput | None
    sessionEntityTypes: List[SessionEntityType] | None

a = WebhookResponse.construct()
a = a.json(exclude_none=True)
print(a)
