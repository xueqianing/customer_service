from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import ActionResult, Action


class CustomAction(Action):
    name = "custom"
    async def run(self,state:DialogueState,action_kwargs:dict[str,Any]):
        print("CustomAction")
        return ActionResult()
