from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult


class CustomAction(Action):
    name = "custom_action"



    async def run(self,state:DialogueState,action_kwargs:dict[str,Any]):
        print("CustomAction")
        return ActionResult()


