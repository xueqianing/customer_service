from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.flow.models import FlowsList
from atguigu.flow.step import FlowStep, StartFlowStep, EndFlowStep, ActionFlowStep, CollectSlotStep
from atguigu.task.action.runner import ActionRunner, ActionCall


class FlowExecutor:
    async def run_task(self,state:DialogueState,flows:FlowsList,action_runner:ActionRunner)->list[BotMessage]:
        messages:list[BotMessage] = []
        while True:
            action_call:ActionCall = self.advance_until_action(state,flows)
            if action_call.action_name == 'action_listen':
                break
            else:
                action_result = await action_runner.run_action(action_call, state)
                state.set_slots(action_result.slots)
                messages.extend(action_result.messages)
        return messages

    def advance_until_action(self, state:DialogueState, flows:FlowsList)->ActionCall:
        while True:
            current_task = state.active_system_task or state.active_task
            if current_task is None:
                return ActionCall(action_name='action_listen')
            flow = flows.get_flow_by_id(current_task.flow_id)
            step = flows.get_step_by_id(current_task.step_id)
            step_result = self.__run_step(step, state)
            if step_result is not None:
                return step_result

    def __run_step(self, step:FlowStep, state:DialogueState)->ActionCall|None:
        if isinstance(step,StartFlowStep):
            pass
        if isinstance(step,EndFlowStep):
            pass
        if isinstance(step,CollectSlotStep):
            pass
        if isinstance(step,ActionFlowStep):
            pass