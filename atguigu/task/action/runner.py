from dataclasses import field, dataclass
from typing import Any

from watchfiles import awatch

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import ActionResult
from atguigu.task.action.registry import ActionRegistry

@dataclass
class ActionCall:
    action_name:str
    action_kwargs:dict[str,Any] = field(default_factory=dict)
@dataclass
class ActionRunner:
    def __init__(self,registry:ActionRegistry) -> None:
        self.registry = registry

    async def run(self,action_call:ActionCall,
                        state:DialogueState) -> ActionResult:
        action_name = action_call.action_name
        action = self.registry.get(action_name)
        return await action.run(state,action_call.action_kwargs)

