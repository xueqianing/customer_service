from atguigu.domain.messages import UserMessage, ProcessResult
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.repository.dialogue_statue_repository import DialogueStateRepository


class DialogueService:
    def __init__(self,
                 dialogue_state_repository:DialogueStateRepository,
                 dialogue_engine:DialogueEngine):
        self.dialogue_state_repository = dialogue_state_repository
        self.dialogue_engine = dialogue_engine

    async def process_message(self,user_message:UserMessage) -> ProcessResult:
        return await self.dialogue_engine.process_message(self.dialogue_state_repository,user_message)



