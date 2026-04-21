from atguigu.domain.messages import UserMessage, ProcessResult
from atguigu.domain.state import DialogueState


class DialogueEngine:
    async def process_message(self, state: DialogueState, user_message: UserMessage) -> ProcessResult:
        pass
