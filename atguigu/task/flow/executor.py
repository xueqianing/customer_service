from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.task.action.base import ActionResult
from atguigu.task.action.runner import ActionCall, ActionRunner
from atguigu.task.flow.models import FlowsList, Flow
from atguigu.task.flow.steps import FlowStep, StartFlowStep, EndFlowStep, CollectSlotStep, ActionFlowStep


class FlowExecutor:

    async def run_task(self, state: DialogueState, flows: FlowsList, action_runner: ActionRunner) -> list[BotMessage]:
        messages: list[BotMessage] = []
        while True:
            action_call: ActionCall = self.advance_until_action(state, flows)
            if action_call.action_name == "action_listen":
                break
            else:
                action_result: ActionResult = await action_runner.run(action_call, state)
                state.set_slots(action_result.slot_updates)
                messages.extend(action_result.messages)
        return messages

    def advance_until_action(self, state: DialogueState, flows: FlowsList) -> ActionCall:
        while True:
            current_task = state.active_system_task or state.active_task  # 系统任务优先
            if current_task is None:
                return ActionCall(action_name="action_listen")

            flow: Flow = flows.get_flow_by_id(current_task.flow_id)
            step: FlowStep = flow.get_step_by_id(current_task.step_id)
            step_result: ActionCall | None = self._run_step(step, state)

            if step_result is not None:
                return step_result

    def _run_step(self, step: FlowStep, state: DialogueState) -> ActionCall | None:
        if isinstance(step, StartFlowStep):
            pass
        if isinstance(step, EndFlowStep):
            pass
        if isinstance(step, CollectSlotStep):
            pass
        if isinstance(step, ActionFlowStep):
            pass
