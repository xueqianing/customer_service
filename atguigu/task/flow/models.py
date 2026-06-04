from dataclasses import dataclass, field
from typing import List, Dict

from atguigu.task.flow.steps import FlowStep


@dataclass
class FlowSlot:
    name:str
    type:str = "any"
    label:str = ""
    description:str = ""


@dataclass
class Flow:
    id:str
    description:str = ""
    steps:List[FlowStep] = field(default_factory=list)
    slots:List[FlowSlot] = field(default_factory=list)
    name:str | None  = None

@dataclass
class FlowsList:
    flows:List[Flow] = field(default_factory=list)
    slots:Dict[str,FlowSlot] = field(default_factory=dict)

