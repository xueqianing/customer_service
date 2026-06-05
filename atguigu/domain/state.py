from dataclasses import dataclass, field
from typing import Any

from atguigu.domain.contexts import TaskContext, SystemContext
from atguigu.domain.messages import UserMessage, BotMessage

@dataclass
class FocusedObject:
    type:str
    id:str
    title:str | None = None
    attributes:dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data:dict[str,Any]) -> "FocusedObject":
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
class Turn:
    turn_id:str
    user_message:UserMessage
    bot_messages:list[BotMessage]

    @classmethod
    def from_dict(cls, data:dict[str,Any]):
        return cls(
            turn_id=data['turn_id'],
            user_message=UserMessage.from_dict(data['user_message']),
            bot_messages=[BotMessage.from_dict(bot_message) for bot_message in data['bot_messages']]
        )

    def to_dict(self):
        return {
            'turn_id': self.turn_id,
            'user_message': self.user_message.to_dict(),
            'bot_messages': [bot_message.to_dict() for bot_message in self.bot_messages]}


@dataclass
class Session:
    session_id:str
    started_at:float
    last_activity_at:float
    closed_at:float | None = None
    turns:list[Turn] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data:dict[str,Any]) -> "Session":
        return cls(
            session_id=data['session_id'],
            started_at=data['started_at'],
            last_activity_at=data['last_activity_at'],
            closed_at=data['closed_at'],
            turns=[Turn.from_dict(turn) for turn in data['turns']]
        )

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'started_at': self.started_at,
            'last_activity_at': self.last_activity_at,
            'closed_at': self.closed_at,
            'turns': [turn.to_dict() for turn in self.turns]
        }


@dataclass
class DialogueState:
    sender_id:str
    active_task:TaskContext | None = None
    paused_tasks:list[TaskContext] = field(default_factory=list)
    active_system_task:SystemContext | None = None
    focused_object:FocusedObject | None = None
    sessions:list[Session] = field(default_factory=list)
    current_session_id:str | None = None
    pending_turn:Turn | None = None

    @classmethod
    def from_dict(cls, data:dict[str,Any]) -> "DialogueState":
        return cls(
            sender_id=data['sender_id'],
            active_task=TaskContext.from_dict(data['active_task']) if data['active_task'] else None,
            paused_tasks=[TaskContext.from_dict(task) for task in data['paused_tasks']],
            active_system_task=SystemContext.from_dict(data['active_system_task']) if data['active_system_task'] else None,
            focused_object=FocusedObject.from_dict(data['focused_object']) if data['focused_object'] else None,
            sessions=[Session.from_dict(session) for session in data['sessions']],
            current_session_id=data['current_session_id'] if 'current_session_id' in data else None,
            pending_turn=Turn.from_dict(data['pending_turn']) if 'pending_turn' in data else None
        )

    def to_dict(self) -> dict[str,Any]:
        return {
            'sender_id': self.sender_id,
            'active_task': self.active_task.to_dict() if self.active_task else None,
            'paused_tasks': [task.to_dict() for task in self.paused_tasks],
            'active_system_task': self.active_system_task.to_dict() if self.active_system_task else None,
            'focused_object': self.focused_object.to_dict() if self.focused_object else None,
            'sessions': [session.to_dict() for session in self.sessions],
            'current_session_id': self.current_session_id,
            'pending_turn': self.pending_turn.to_dict() if self.pending_turn else None
        }
    def current_session_id(self) -> Session | None:
        for session in self.sessions:
            if session.session_id == self.current_session_id:
                return session
        return None

    def set_slots(self, slot:dict[str,Any]):
        self.active_task.slots.update(slot)

    def current_task(self):
        return self.active_system_task or self.active_task

    def end_system_task(self):
        self.active_system_task = None

    def end_active_task(self):
        self.active_task = None

    def remove_slot(self, slot_name):
        self.active_task.slots.pop(slot_name)

    def start_system_task(self,system_context:SystemContext):
        self.active_system_task = system_context







