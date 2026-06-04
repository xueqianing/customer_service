from dataclasses import dataclass, field, fields
from enum import Enum
from typing import List, Any

from atguigu.task.flow.links import FlowStepLink


class FlowStepType(Enum):
    START = 'start'
    ACTION = 'action'
    COLLECT = 'collect'
    END = 'end'


@dataclass
class ResponseDefinition:
    mode: str = "static"
    text:str | None = None
    prompt:str | None = None

@dataclass
class SlotValidation:
    condition:str | None = None
    failure_response:ResponseDefinition | None = None

@dataclass
class FlowStep:
    id:str = ""
    type:FlowStepType = FlowStepType.START
    next:List[FlowStepLink] = field(default_factory=list)
    description:str | None = None

    @classmethod
    def from_dict(cls, step_data:dict[str,Any]):
        step_type = step_data['type']
        clz = STEP_TYPE_TO_CLASS[step_type]
        # 过滤出目标类声明的 dataclass 字段，避免传入未知参数报错
        field_names = {f.name for f in fields(clz)}
        kwargs = {k: v for k, v in step_data.items() if k in field_names}
        return clz(**kwargs)


class StartFlowStep(FlowStep):
    pass


@dataclass
class ActionFlowStep(FlowStep):
    action:str = ""
    slots:List[str] = field(default_factory=list)


@dataclass
class CollectSlotStep(FlowStep):
    slot_name:str = ""
    response:ResponseDefinition = field(default_factory=ResponseDefinition)
    validation:SlotValidation | None = None


class EndFlowStep(FlowStep):
    pass



STEP_TYPE_TO_CLASS = {
    "start": StartFlowStep,
    "action": ActionFlowStep,
    "collect": CollectSlotStep,
    "end": EndFlowStep
}

