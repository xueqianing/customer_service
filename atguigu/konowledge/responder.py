from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt, PromptTemplate

from atguigu.api.routers.chat_router import history
from atguigu.domain.messages import UserMessage, BotMessage
from atguigu.domain.state import Turn
from atguigu.infrastructure import llm
from atguigu.konowledge.provider import KnowledgeChunk
from atguigu.prompts.history_builder import HistoryBuilder


class KnowledgeResponder:
    async def respond(self,user_message:UserMessage,recent_turns:list[Turn],chunks:list[KnowledgeChunk]) -> list[BotMessage]:
        user_message = HistoryBuilder._render_user_message(recent_turns)
        knowledge_content = "\n\n".join(chunk.content for chunk in chunks)
        prompt_text = load_prompt("knowledge_respond")
        prompt = PromptTemplate.from_template(
            prompt_text,
            template_format="jinja2"
        )
        chain = prompt | llm | StrOutputParser()

        response = await chain.ainvoke(
            {"user_message": user_message, "history": history, "knowledge_content": knowledge_content})
        return [BotMessage(text=response)]