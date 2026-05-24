from itertools import chain
from typing import Any

from jinja2 import Template
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.infrastructure.llm import llm
from atguigu.task.action.base import Action, ActionResult


class ActionResponse(Action):
    name = 'action_response'
    async def run(self,
                  state:DialogueState,
                  action_kwargs:dict[str,Any]) -> ActionResult:
        model = action_kwargs.get('mode','static')
        if model == 'static':
            text = action_kwargs['text']
            render_text = self.render_text(text, state)
            return ActionResult(messages=[BotMessage(text=render_text)])
        elif model == 'rephrase':
            text = action_kwargs['text']
            rendered_text = self._rander_text(text,state)
            prompt_text = action_kwargs['prompt']
            llm_message = await self._call_llm(prompt_text,state,rendered_text)
            return ActionResult(messages=[BotMessage(text=llm_message)])
        else:
            prompt_text = action_kwargs['prompt']
            message = await self._call_llm(prompt_text, state)
            return ActionResult(messages=[BotMessage(text=message)])

    def render_text(self, text:str, state:DialogueState):
        template = Template(text)
        result = template.render(slots=state.active_task.slots, context=state.active_system_task or state.active_task)
        return result

    async def _call_llm(self, prompt_text:str, state:DialogueState, rendered_text:str="")-> str:
        prompt = PromptTemplate.from_template(prompt_text, template_format="jinja2")
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        bot_message = await chain.ainvoke({
                "history": HistoryBuilder.build(state.current_session().turns),
                "user_message": HistoryBuilder._render_user_message(state.pending_turn.user_message),
                "current_response": rendered_text
            })

