from typing import Dict

from atguigu.task.action.base import Action


class ActionRegistry:
    def __init__(self):
        self._actions:Dict[str,Action] = {}

    def register(self,action:Action):
        self._actions[action.name] =action


    def get_action(self, action_name: str):
        return self._actions[action_name]