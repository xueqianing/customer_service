from dataclasses import asdict
from typing import List

from atguigu.domain.contexts import CollectSystemContext
from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.task.flow.links import FlowStepLink, StaticLink, ConditionalLink, FallbackLink
from atguigu.task.flow.models import FlowsList
from atguigu.task.flow.step import FlowStep, StartFlowStep, EndFlowStep, ActionFlowStep, CollectSlotStep
from atguigu.task.action.runner import ActionRunner, ActionCall


def _eval_condition(condition: str, state: DialogueState) -> bool:
    data = {
        "slots": state.active_task.slots,
        "context": asdict(state.current_task())
    }
    return bool(eval(condition, {}, data))


def _select_next_step(step:FlowStep, state:DialogueState):
    links:List[FlowStepLink] = step.next
    for link in links:
        if isinstance(link,StaticLink):
            return link.target
        if isinstance(link,ConditionalLink):
            if _eval_condition(link.condition,state):
                return link.target
        if isinstance(link,FallbackLink):
            return link.target
    return None





class FlowExecutor:
    async def run_task(self,state:DialogueState,flows:FlowsList,action_runner:ActionRunner)->list[BotMessage]:
        messages:list[BotMessage] = []
        while True:
            action_call:ActionCall = self._advance_until_action(state,flows)
            if action_call.action_name == 'action_listen':
                break
            else:
                action_result = await action_runner.run_action(action_call, state)
                state.set_slots(action_result.slots)
                messages.extend(action_result.messages)
        return messages

    def _advance_until_action(self, state:DialogueState, flows:FlowsList)->ActionCall:
        while True:
            current_task = state.active_system_task or state.active_task
            if current_task is None:
                return ActionCall(action_name='action_listen')
            flow = flows.get_flow_by_id(current_task.flow_id)
            step = flows.get_step_by_id(current_task.step_id)
            step_result = self.__run_step(step, state)
            if step_result is not None:
                return step_result

    def __run_step(self, step:FlowStep, state:DialogueState,flows:FlowsList)->ActionCall|None:
        if isinstance(step,StartFlowStep):
            return self.__run_start_step(step, state)
        if isinstance(step,EndFlowStep):
            self._run_end_step(state)
        if isinstance(step,CollectSlotStep):
            self._run_collect_step(step, state,flows)
        if isinstance(step,ActionFlowStep):
            self._run_action_step(step,state)
        return None

    def __run_start_step(self, step:StartFlowStep, state:DialogueState):
        return self._advance_to_next_step(step, state)

    def _advance_to_next_step(self,step: FlowStep, state: DialogueState):
        next_step_id = _select_next_step(step, state)
        state.current_task().step_id = next_step_id

    def _run_end_step(self, state:DialogueState):
        if state.active_system_task:
            state.end_system_task()
            return None
        else:
            state.end_active_task()
            return None

    def _run_collect_step(self, step:CollectSlotStep, state:DialogueState, flows:FlowsList):
        self._try_to_fill_slot_from_focused_object(step, state)
        if state.active_task.slots.get(step.slot_name):
            if step.validation:
                condition = step.validation.condition
                if self._eval_condition(condition,state):
                   self._advance_to_next_step(step, state)
                   return None
                else:
                    state.remove_slot(step.slot_name)
                    if step.validation.failure_response:
                        return ActionCall(action_name="action_response",
                                          action_kwargs=asdict(step.validation.failure_response))
                    else:
                        return None
            else:
                state.start_system_task(CollectSystemContext(
                    flow_id="system_collect_information",
                    step_id=flows.get_flow_by_id("system_collect_information").start_step().id,
                    slot_name=step.slot_name,
                    response=asdict(step.response)
                ))




    def _try_to_fill_slot_from_focused_object(self, step:CollectSlotStep, state:DialogueState):
        if state.focused_object is None:
            return
        if step.slot_name == 'order_number' and state.focused_object.type == 'order':
            state.set_slots({step.slot_name: state.focused_object.id})
        if step.slot_name == 'product_id' and state.focused_object.type == 'product':
            state.set_slots({step.slot_name: state.focused_object.id})

    def _run_action_step(self, step:ActionFlowStep, state:DialogueState)->ActionCall | None:
        self._advance_to_next_step(step, state)
        action_call = self._build_action_call(step, state)
        return action_call

    def _build_action_call(self, step:ActionFlowStep, state:DialogueState):
        action_name = step.action
        args = step.args
        if isinstance(args,str):
            args =asdict(state.current_task())[args.split('.')][1]
        return ActionCall(action_name=action_name,action_kwargs=args)






