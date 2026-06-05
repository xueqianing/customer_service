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

@dataclass
class StartedSystemContext(SystemContext):
    started_flow_id:str = ""
    started_flow_name:str = ""
@dataclass
class InterruptedSystemContext(SystemContext):
    interrupted_flow_id:str =""
    interrupted_flow_name:str = ""
    started_flow_id:str = ""
    started_flow_name:str = ""
@dataclass
class CanceledSystemContext(SystemContext):
    canceled_flow_id:str = ""
    canceled_flow_name:str = ""
@dataclass
class ResumedSystemContext(SystemContext):
    resumed_flow_id:str = ""
    resumed_flow_name:str = ""

class CollectSystemContext(SystemContext):
    slot_name:str = ""
    response:dict[str,Any] = field(default_factory=dict)


FLOW_ID_TO_CONTEXT_CLASS = {
    "system_task_started": StartedSystemContext,
    "system_task_interrupted": InterruptedSystemContext,
    "system_task_canceled": CanceledSystemContext,
    "system_task_resumed": ResumedSystemContext,
    "system_collect_information": CollectSystemContext
}



    