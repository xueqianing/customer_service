from dataclasses import dataclass, field

from atguigu.flow.step import FlowStep


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


@dataclass
class FlowsList:
    flows: list[Flow] = field(default_factory=list)
    slots: dict[str, FlowSlot] = field(default_factory=dict)
