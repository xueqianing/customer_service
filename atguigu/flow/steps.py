from dataclasses import dataclass, field
from enum import Enum
from typing import List

from atguigu.flow.links import FlowStepLink


class FlowStepType(Enum):
    START = 'start'
    ACTION = 'action'
    COLLECT = 'collect'
    END = 'end'


class ResponseDefinition:
    mode: str = "static"
    text:str | None = None
    prompt:str | None = None

@dataclass
class SlotValidation:
    condition:str | None = None
    failure_response:ResponseDefinition | None = None

class FlowStep:
    id:str
    type:FlowStepType
    next:List[FlowStepLink] = field(default_factory=list)
    description:str | None = None


class StartFlowStep(FlowStep):
    pass

class ActionFLowStep(FlowStep):
    action:str
    slots:List[str] = field(default_factory=list)

class CollectionSlotStep(FlowStep):
    slot_name:str = ""
    response:ResponseDefinition = field(default_factory=ResponseDefinition)
    validation:SlotValidation | None = None

class EndFlowStep(FlowStep):
    pass


