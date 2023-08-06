from typing import Dict
from enum import Enum

from pydantic import BaseModel


class Platform(Enum):
    PLATFORM_UNSPECIFIED = "PLATFORM_UNSPECIFIED"
    FACEBOOK = "FACEBOOK"
    SLACK = "SLACK"
    TELEGRAM = "TELEGRAM"
    KIK = "KIK"
    SKYPE = "SKYPE"
    LINE = "LINE"
    VIBER = "VIBER"
    ACTIONS_ON_GOOGLE = "ACTIONS_ON_GOOGLE"
    GOOGLE_HANGOUTS = "GOOGLE_HANGOUTS"


class Message(BaseModel):
    platform: Platform | None
    text: dict | None
    image: dict | None
    quickReplies: dict | None
    card: dict | None
    payload: dict | None
    simpleResponses: dict | None
    basicCard: dict | None
    suggestions: dict | None
    linkOutSuggestion: dict | None
    listSelect: dict | None
    carouselSelect: dict | None
    browseCarouselCard: dict | None
    tableCard: dict | None
    mediaContent: dict | None

    class Config:
        use_enum_values = True


class Context(BaseModel):
    name: str
    lifespanCount: int | None
    parameters: Dict[str, str | int | bool | None | list | dict] | None
