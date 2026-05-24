from dataclasses import dataclass, field

from atguigu.flow.step import FlowStep, FlowStepType


@dataclass
class FlowSlot:
    name: str
    type: str = "any"
    label: str = ""
    description: str = ""


@dataclass
class Flow:
    id: str
    description: str = ""
    steps: list[FlowStep] = field(default_factory=list)
    slots: list[FlowSlot] = field(default_factory=list)
    name: str | None = None

    def start_step(self) -> FlowStep|None:
        for step in self.steps:
            if step.type == FlowStepType.START:
                return step
        return None

@dataclass
class FlowsList:
    flows: list[Flow] = field(default_factory=list)
    slots: dict[str, FlowSlot] = field(default_factory=dict)

    def get_flow_by_id(self, flow):
        for flow in self.flows:
            if flow.id == flow.id:
                return flow
        return None

    def get_step_by_id(self, step_id: str) -> FlowStep | None:
        for step in self.steps:
            if step.id == step_id:
                return step
        return None