
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from atguigu.flow.links import FlowStepLink


class FlowStepType(Enum):
    START = "start"
    ACTION = "action"
    COLLECT = "collect"
    END = "end"


class ResponseDefinition:
    mode:str ="static"
    text:str | None = None
    prompt:str | None = None


class SlotValidation:
    condition:str | None = None
    failure_response:ResponseDefinition | None = None


@dataclass
class FlowStep:
    id:str
    type:FlowStepType
    next:List[FlowStepLink] = field(default_factory=list)
    description:str = ""

