from dill import settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine


def init_db_engine():
    global  engine,session_factory
    engine = create_async_engine(settings.database_url)
    session_factory = async_sessionmaker(engine,expire_on_commit = False)

async  def close_db_engine():
    await engine.dispose()



