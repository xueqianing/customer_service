from tkinter.filedialog import dialogstates

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.domain.state import DialogueState
from atguigu.models.DialogueStateRecord import DialogueStateRecord


class DialogueStateRepository:
    def __init__(self,session:AsyncSession):
        self.session = session
    async def load_state(self,sender_id:str):
        sql = select(DialogueStateRecord).where(DialogueStateRecord.sender_id == sender_id)
        result = await self.session.execute(sql)
        state = result.scalar_one_or_none()
        if state:
            dialogue_state:DialogueState = None
            return dialogue_state
        else:
            return DialogueState(sender_id=sender_id)

    async def save_state(self, state):
        pass