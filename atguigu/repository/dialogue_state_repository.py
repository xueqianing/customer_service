from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.domain.state import DialogueState
from atguigu.models.dialogue_state import DialogueStateRecord


class DialogueStateRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def load_state(self, sender_id: str) -> DialogueState:
        sql = select(DialogueStateRecord).where(DialogueStateRecord.sender_id == sender_id)
        result = await self.session.execute(sql)
        state = result.scalar_one_or_none()
        if state:
        # todo: 将state。state_json 反序列化成一个DialogueState对象
            dialogue_state:DialogueState = None
            return dialogue_state
        else:
            return DialogueState(sender_id=sender_id)

    async def save_state(self, state: DialogueState):
        # todo: 将state序列化为一个json字符串
        state_json: str = "{}"
        insert_stmt = insert(DialogueStateRecord).values(
            sender_id=state.sender_id, state_json=state_json
        )
        upsert_stmt = insert_stmt.on_duplicate_key_update(
            state_json=insert_stmt.inserted.state_json
        )

        await self.session.execute(upsert_stmt)
        await self.session.commit()
