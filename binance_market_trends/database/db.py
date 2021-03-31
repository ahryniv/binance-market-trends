import gino
import sqlalchemy

from binance_market_trends.conf.settings import settings

db = gino.Gino()


async def init_db():
    engine = await sqlalchemy.create_engine(settings.sqlalchemy_database_uri, strategy='gino')
    db.bind = engine


async def disconnect_db():
    engine, db.bind = db.bind, None
    await engine.close()
