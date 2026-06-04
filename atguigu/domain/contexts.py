from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskContext:
    flow_id:str
    step_id:str | None = None
    slots:dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data:dict[str,Any])-> "TaskContext":
        return cls(
            flow_id=data['flow_id'] ,
            step_id=data['step_id'],
            slots=data['slots'] 
        )

    def to_dict(self):
        return {
            'flow_id':self.flow_id,
            'step_id':self.step_id,
            'slots':self.slots
        }


@dataclass
class SystemContext:
    flow_id:str
    step_id:str | None = None

    @classmethod
    def from_dict(cls, data:dict[str,Any])-> "SystemContext":
        return cls(
            flow_id=data['flow_id'] ,
            step_id=data['step_id']
        )

    def to_dict(self):
        return {
            'flow_id':self.flow_id,
            'step_id':self.step_id
        }
    