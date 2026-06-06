from tornado.gen import sleep
from watchfiles import awatch

from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.knowledge.intents import KnowledgeIntent
from atguigu.knowledge.providers import KnowledgeChunk
from atguigu.knowledge.registry import KnowledgeProviderRegistry
from atguigu.knowledge.responder import KnowledgeResponder


class KnowledgeHandler:
    def __init__(self, knowledge_intents: dict[str, KnowledgeIntent],
                 provider_registry: KnowledgeProviderRegistry,
                 knowledge_responder: KnowledgeResponder):
        self.knowledge_intents = knowledge_intents
        self.provider_registry = provider_registry
        self.knowledge_responder = knowledge_responder
    async def handle(self,intents:list[str],state:DialogueState) -> list[BotMessage]:
        provider_ids:list[str] = self._get_provider_ids_by_intents(intents)
        chunks:list[KnowledgeChunk] = []
        # 获取知识
        chunks: list[KnowledgeChunk] = []
        for provider_id in provider_ids:
            provider = self.provider_registry.get(provider_id)
            current_chunks = await provider.retrieve(state)
            chunks.extend(current_chunks)
        return await self.knowledge_responder.respond(
            user_message=state.pending_turn.user_message,
            recent_turns=state.current_session().turns,
            chunks=chunks
        )


    def _get_provider_ids_by_intents(self,intents:list[str]) -> list[str]:
        provider_ids:list[str] = []
        for intent in intents:
            if intent in self.knowledge_intents:
                provider_ids.extend(self.knowledge_intents[intent].provider_ids)
        return provider_ids

