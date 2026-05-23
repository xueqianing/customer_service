from atguigu.common.models import Command, StartFlowCommand, SetSlotsCommand, CancelFlowCommand, ResumeFlowCommand
from atguigu.domain.contexts import TaskContext, InterruptedSystemContext, StartedSystemContext, CanceledSystemContext, \
    ResumedSystemContext
from atguigu.domain.state import DialogueState
from atguigu.flow.models import FlowsList, Flow


class CommonProcessor:
    def run(self,
            commands:list[Command],
            state:DialogueState,
            flows:FlowsList) ->None:
        for command in commands:
            self._apply(command,state,flows)

    def _apply(self, command:Command, state:DialogueState, flows:FlowsList)->None:
        if isinstance(command,StartFlowCommand):
            self._handle_start_flow(command,state,flows)
        elif isinstance(command, SetSlotsCommand):
            self._handle_set_slots(command,state,flows)
        elif isinstance(command,CancelFlowCommand):
            self._handle_cancel_flow(command,state,flows)
        elif isinstance(command,ResumeFlowCommand):
            self._handle_resume_flow(command,state,flows)

    @staticmethod
    def _handle_start_flow( command:StartFlowCommand, state:DialogueState, flows:FlowsList)->None:
        state.end_system_task()
        target_flow = flows.get_flow_by_id(command.flow)
        active_task = state.active_task
        if active_task:
            state.interrupt_active_task()
            state.start_task(TaskContext(
                flow_id=active_task.flow_id,
                step_id=active_task.step_id
            ))
            state.start_system_task(InterruptedSystemContext(
                flow_id="system_task_interrupted",
                step_id=flows.get_flow_by_id("system_task_interrupted").start_step().id,
                interrupted_flow_id=active_task.flow_id,
                interrupted_flow_name=flows.get_flow_by_id(active_task.flow_id).name,
                started_flow_id=target_flow.id,
                started_flow_name=target_flow.name
            ))
        else:
            state.start_task(TaskContext(
                flow_id=target_flow.id,
                step_id=target_flow.start_step().id
            ))
            state.start_system_task(StartedSystemContext(
                flow_id="system_task_started",
                step_id=flows.get_flow_by_id("system_task_started").start_step().id,
                started_flow_name= target_flow.name,
                started_flow_id=target_flow.id
            ))


    @staticmethod
    def _handle_set_slots(command:SetSlotsCommand, state:DialogueState, flows:FlowsList)->None:
        if state.active_task:
            state.set_slots(command.slots)

    @staticmethod
    def _handle_cancel_flow(command:CancelFlowCommand, state:DialogueState, flows:FlowsList)->None:
        active_task = state.active_task
        target_flow = flows.get_flow_by_id(active_task.flow_id)
        state.cancel_active_task()
        state.start_system_task(CanceledSystemContext(
            flow_id="system_task_canceled",
            step_id=flows.get_flow_by_id("system_task_canceled").start_step().id,
            canceled_flow_id=active_task.flow_id,
            canceled_flow_name=target_flow.name
        ))


    @staticmethod
    def _handle_resume_flow( command:ResumeFlowCommand, state:DialogueState, flows:FlowsList)->None:
        target_flow: Flow = flows.get_flow_by_id(command.flow)
        active_task:TaskContext =  state.active_task
        if active_task:
            if active_task.flow_id == target_flow.id:
                return
            else:
                state.interrupt_active_task()
                state.start_system_task(InterruptedSystemContext(
                    flow_id="system_task_interrupted",
                    step_id=flows.get_flow_by_id("system_task_interrupted").start_step().id,
                    interrupted_flow_id=active_task.flow_id,
                    interrupted_flow_name=flows.get_flow_by_id(active_task.flow_id).name,
                    started_flow_id=target_flow.id,
                    started_flow_name=target_flow.name
                ))
        else:
            state.resume_task(target_flow.id)
            state.start_system_task(ResumedSystemContext(
                flow_id="system_task_resumed",
                step_id=flows.get_flow_by_id("system_task_resumed").start_step().id,
                resumed_flow_id=target_flow.id,
                resumed_flow_name=target_flow.name
            ))


