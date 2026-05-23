from atguigu.domain.messages import UserMessage, ProcessResult


class DialogueEngine:
    async def process_message(self,DialogueState,
                              user_message:UserMessage)-> ProcessResult:
        pass