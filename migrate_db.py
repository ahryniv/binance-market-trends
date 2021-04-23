import os

from alembic import command
from alembic.config import Config

from binance_market_trends.conf.settings import settings


def migrate_db(sqlalchemy_database_uri: str):
    os.environ['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
    current_path = os.path.dirname(os.path.realpath(__file__))
    migrations_path = os.path.join(current_path, 'binance_market_trends', 'database', 'migrations')
    config_path = os.path.join(current_path, 'alembic.ini')
    alembic_cfg = Config(config_path)
    alembic_cfg.set_main_option('script_location', migrations_path)
    command.upgrade(alembic_cfg, 'head')


if __name__ == '__main__':
    migrate_db(sqlalchemy_database_uri=settings.sqlalchemy_database_uri)
