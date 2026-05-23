import asyncio
import json

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.domain.contexts import TaskContext
from atguigu.domain.state import DialogueState
from atguigu.infrastructure import database
from atguigu.infrastructure.database import init_db_engine, close_db_engine
from atguigu.models.dialogue_status import DialogueStateRecord


class DialogueStateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def load_state(self, sender_id: str) -> DialogueState:
        sql = select(DialogueStateRecord).where(
            DialogueStateRecord.sender_id == sender_id
        )
        result = await self.session.execute(sql)
        state = result.scalar_one_or_none()
        if state:
            # 将state.state_json 反序列化成一个DialogueState对象
            dialogue_state: DialogueState = DialogueState.from_dict(
                json.loads(state.state_json)
            )
            return dialogue_state
        else:
            return DialogueState(sender_id=sender_id)

    async def save_state(self, state: DialogueState):
        state_json = json.dumps(state.to_dict(), ensure_ascii=False)

        insert_stmt = insert(DialogueStateRecord).values(
            sender_id=state.sender_id, state_json=state_json
        )
        upsert_stmt = insert_stmt.on_duplicate_key_update(
            state_json=insert_stmt.inserted.state_json
        )

        await self.session.execute(upsert_stmt)
        await self.session.commit()


if __name__ == "__main__":
    init_db_engine()

    async def test():
        # 确保表已创建
        async with database.engine.begin() as conn:
            await conn.run_sync(DialogueStateRecord.metadata.create_all)

        async with database.session_factory() as session:
            repo = DialogueStateRepository(session)

            state = DialogueState(
                sender_id="test_sender",
                active_task=TaskContext(
                    flow_id="flow-1", step_id="step-1", slots={"order_id": "order-1"}
                ),
            )
            await repo.save_state(state)

            loaded_state = await repo.load_state("test_sender")
            print("loaded_state:", loaded_state)
            print("active_task:", loaded_state.active_task)
            print("slots:", loaded_state.active_task.slots if loaded_state.active_task else None)
        await close_db_engine()

    asyncio.run(test())
