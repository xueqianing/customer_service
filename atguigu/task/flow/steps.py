from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any

from atguigu.task.flow.links import FlowStepLink


class FlowStepType(Enum):
    START = "start"
    ACTION = "action"
    COLLECT = "collect"
    END = "end"


@dataclass(slots=True)
class ResponseDefinition:
    mode: str = "static"
    text: str | None = None
    prompt: str | None = None


@dataclass(slots=True)
class SlotValidation:
    condition: str | None = None
    failure_response: ResponseDefinition | None = None


@dataclass(slots=True)
class FlowStep:
    id: str
    type: FlowStepType
    next: List[FlowStepLink] = field(default_factory=list)
    description: str = ""


@dataclass(slots=True)
class StartFlowStep(FlowStep):
    pass


@dataclass(slots=True)
class ActionFlowStep(FlowStep):
    action: str = ""
    args: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CollectSlotStep(FlowStep):
    slot_name: str = ""
    response: ResponseDefinition = field(default_factory=ResponseDefinition)
    validation: SlotValidation | None = None


@dataclass(slots=True)
class EndFlowStep(FlowStep):
    pass
