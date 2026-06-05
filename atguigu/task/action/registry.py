from typing import Dict

from atguigu.task.action.base import Action


class ActionRegistry:
    def __init__(self) -> None:
        self._actions:Dict[str,Action] = {}
    def register(self,action:Action ) -> None:
        self._actions[action.name] = action
    def get(self, action_name: str)-> Action:
        if action_name not in self._actions:
               raise ValueError(f"Action {action_name} not registered")
        return self._actions[action_name]
