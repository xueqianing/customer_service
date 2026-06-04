import uuid

from fastapi import APIRouter
from fastapi.params import Depends

from atguigu.api.dependencies import get_dialogue_service
from atguigu.api.schemas import ChatResponse, ChatRequest, HistoryResponse, ChatBotMessage, ChatObject, HistoryMessage
from atguigu.domain.messages import ProcessResult, UserMessage, MessageType, MessageObject, BotMessage
from atguigu.service.dialogue_service import DialogueService

chat_router = APIRouter()


def _build_ser_message(chat_request:ChatRequest)-> UserMessage:
    return UserMessage(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id or str(uuid.uuid4()),
        type = MessageType.TEXT if chat_request.text else MessageType.OBJECT,
        text = chat_request.text,
        object=MessageObject(type = chat_request.object.type,
                             id = chat_request.object.id,
                             attributes = chat_request.object.attributes) if chat_request.object else None
    )


def _build_chat_response(process_result):
    return ChatResponse(
        message_id = process_result.message_id,
        sender_id = process_result.sender_id,
        messages=[ChatBotMessage(
            text = message.text,
            object = ChatObject(
                type=message.object.type,
                id=message.object.id,
                attributes=message.object.attributes
            ) if message.object else None ) for message in process_result.messages]
    )


@chat_router.post('/api/chat')
async def chat(
        chat_request:ChatRequest,
        dialogue_service:DialogueService = Depends(get_dialogue_service)
) -> ChatResponse:
    process_result: ProcessResult = await dialogue_service.process_message(_build_ser_message(chat_request))
    return _build_chat_response(process_result)

@chat_router.get('/api/chat/history')
async def history(sender_id:str) -> HistoryResponse:
    return HistoryResponse(
        sender_id=sender_id,
        messages=[HistoryMessage(
            role = 'user',
            text = 'hello',
            object = ChatObject(
                type='text',
                id='1',
                attributes={}
            )
        ),
        HistoryMessage(
            role = 'bot',
            text = 'hello',
            object = ChatObject(
                type='text',
                id='1',
                attributes={}
            )
        )]

    )