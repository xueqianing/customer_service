from dataclasses import field, dataclass
from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.registry import ActionRegistry


@dataclass
class ActionCall:
    action_name:str
    action_kwargs:dict[str,Any] = field(default_factory=dict)





class ActionRunner:
    def __init__(self,registry:ActionRegistry):
        self.registry = registry

        async def run_action(action_call:ActionCall,state:DialogueState):
            action_name = action_call.action_name
            action = self.registry.get_action(action_name)
            return await action.run(state,action_call.action_kwargs)
