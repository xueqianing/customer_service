from fastapi import APIRouter

from atguigu.api.dependencies import get_dialogue_service
from atguigu.api.schemas import ChatRequest, ChatResponse, HistoryResponse, HistoryMessage
from atguigu.domain.messages import ProcessResult, MessageType, MessageObject, UserMessage
from atguigu.service.dialogue_service import DialogueService
from fastapi.params import Depends
chat_router = APIRouter()
@chat_router.post('/api/chat')
async def chat(
        chat_request:ChatRequest,
        dialogue_service:DialogueService = Depends(get_dialogue_service)) -> ChatResponse:
    user_message = UserMessage(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id,
        type=MessageType.TEXT,
        text=chat_request.text,
        object = MessageObject(
            type=chat_request.object.type,
            id=chat_request.object.id,
            title=chat_request.object.title,
            attributes=chat_request.object.attributes
        )
    )
    process_result:ProcessResult = await dialogue_service.process_message(user_message)
    return ChatResponse(
        sender_id=process_result.sender_id,
        message_id=process_result.message_id,
        messages=[
            ChatResponse.Message(
                text=bot_message.text,
                object=bot_message.object
            ) for bot_message in process_result.messages
        ]
    )



@chat_router.get('/api/chat/history')
async def history(sender_id: str) -> HistoryResponse:
    return HistoryResponse(
        sender_id=sender_id,
        messages=[
            HistoryMessage(
                role='user',
                text='你好'
            ),
            HistoryMessage(
                role='bot',
                text='我不好'
            )
        ]
    )
