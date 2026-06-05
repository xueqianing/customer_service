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

    def get_step_by_id(self, step_id:str):
        for step in self.steps:
            if step.id == step_id:
                return step
        return None


@dataclass
class FlowsList:
    flows:List[Flow] = field(default_factory=list)
    slots:Dict[str,FlowSlot] = field(default_factory=dict)

    def get_flow_by_id(self, flow_id:str) -> Flow | None:
        for flow in self.flows:
            if flow.id == flow_id:
                return flow
        return None

