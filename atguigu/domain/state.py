from dataclasses import field, dataclass
from typing import Any

from atguigu.domain.contexts import TaskContext, SystemContext
from atguigu.domain.messages import BotMessage, UserMessage


@dataclass
class FocusedObject:
    type: str
    id: str
    title: str | None = None
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "id": self.id,
            "title": self.title,
            "attributes": self.attributes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FocusedObject":
        return cls(
            type=data["type"],
            id=data["id"],
            title=data.get("title"),
            attributes=data.get("attributes", {}),
        )


@dataclass
class Turn:
    turn_id: str
    user_message: UserMessage
    bot_messages: list[BotMessage]

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "user_message": self.user_message.to_dict(),
            "bot_messages": [bm.to_dict() for bm in self.bot_messages],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Turn":
        return cls(
            turn_id=data["turn_id"],
            user_message=UserMessage.from_dict(data["user_message"]),
            bot_messages=[BotMessage.from_dict(bm) for bm in data.get("bot_messages", [])],
        )


@dataclass
class Session:
    session_id: str
    started_at: float
    last_activity_at: float
    closed_at: float
    turns: list[Turn] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "last_activity_at": self.last_activity_at,
            "closed_at": self.closed_at,
            "turns": [t.to_dict() for t in self.turns],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Session":
        return cls(
            session_id=data["session_id"],
            started_at=data["started_at"],
            last_activity_at=data["last_activity_at"],
            closed_at=data["closed_at"],
            turns=[Turn.from_dict(t) for t in data.get("turns", [])],
        )


@dataclass
class DialogueState:
    sender_id: str
    active_task: TaskContext | None = None
    paused_tasks: list[TaskContext] = field(default_factory=list)
    active_system_task: SystemContext | None = None
    focused_object: FocusedObject | None = None
    sessions: list[Session] = field(default_factory=list)
    current_session_id: str | None = None,
    pending_turn :Turn| None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sender_id": self.sender_id,
            "active_task": self.active_task.to_dict() if self.active_task else None,
            "paused_tasks": [pt.to_dict() for pt in self.paused_tasks],
            "active_system_task": self.active_system_task.to_dict() if self.active_system_task else None,
            "focused_object": self.focused_object.to_dict() if self.focused_object else None,
            "sessions": [s.to_dict() for s in self.sessions],
            "current_session_id": self.current_session_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DialogueState":
        active_task = data.get("active_task")
        active_system_task = data.get("active_system_task")
        focused_object = data.get("focused_object")
        return cls(
            sender_id=data["sender_id"],
            active_task=TaskContext.from_dict(active_task) if active_task else None,
            paused_tasks=[TaskContext.from_dict(pt) for pt in data.get("paused_tasks", [])],
            active_system_task=SystemContext.from_dict(active_system_task) if active_system_task else None,
            focused_object=FocusedObject.from_dict(focused_object) if focused_object else None,
            sessions=[Session.from_dict(s) for s in data.get("sessions", [])],
            current_session_id=data.get("current_session_id"),
        )

    def end_system_task(self):
        self.active_system_task = None


    def interrupt_active_task(self):
        self.active_task = None
        self.paused_tasks.append(self.active_task)

    def start_task(self, taskContext:TaskContext):
        self.active_task = taskContext

    def start_system_task(self, systemContext:SystemContext):
        self.active_system_task = systemContext

    def set_slots(self, slots):
        self.active_task.slots.update( slots)

    def cancel_active_task(self):
        self.active_task = None
        self.active_system_task = None

    def resume_task(self, id):
        for paused_task in self.paused_tasks:
            if paused_task.flow_id == id:
                self.active_task = paused_task
                self.paused_tasks.remove(paused_task)
                break

    def current_session(self) -> Session | None:
        for session in self.sessions:
            if session.session_id == self.current_session_id:
                return session
        return None
