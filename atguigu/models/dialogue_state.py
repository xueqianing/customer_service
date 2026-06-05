from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.testing.schema import mapped_column

from atguigu.models.Base import Base


class DialogueStateRecord(Base):
    __tablename__ = "dialogue_states"

    sender_id:Mapped[str] = mapped_column(String(255), primary_key = True)
    state_json:Mapped[str] = mapped_column(Text,nullable =  False,default ="{}")
