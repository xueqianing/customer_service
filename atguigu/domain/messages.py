from dataclasses import field, dataclass
from enum import Enum
from typing import Any


class MessageType(Enum):
    TEXT = 'text'
    OBJECT = 'object'


@dataclass
class MessageObject:
    type:str
    id:str
    title:str | None = None
    attributes:dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data:dict[str,Any]):
        return cls(
            type=data['type'],
            id=data['id'],
            title=data['title'],
            attributes=data['attributes']
        )

    def to_dict(self):
        return {
            'type': self.type,
            'id': self.id,
            'title': self.title,
            'attributes': self.attributes
        }


@dataclass
class UserMessage:
    sender_id:str
    message_id:str
    type:MessageType
    text:str | None = None
    object:MessageObject | None = None

    @classmethod
    def from_dict(cls, data:dict[str,Any]):
        return cls(
            sender_id=data['sender_id'],
            message_id=data['message_id'],
            type=MessageType(data['type']),
            text=data['text'],
            object=MessageObject.from_dict(data['object']) if data['object'] else None
        )

    def to_dict(self):
        return {
            'sender_id': self.sender_id,
            'message_id': self.message_id,
            'type': self.type.value,
            'text': self.text,
            'object': self.object.to_dict() if self.object else None
        }


@dataclass
class BotMessage:
    text:str | None = None
    object:MessageObject | None = None

    @classmethod
    def from_dict(cls, data:dict[str,Any]):
        return cls(
            text=data['text'],
            object=MessageObject.from_dict(data['object']) if data['object'] else None
        )

    def to_dict(self):
        return {
            'text': self.text,
            'object': self.object.to_dict() if self.object else None
        }


@dataclass
class ProcessResult:
    sender_id:str
    message_id:str
    messages:list[BotMessage]
