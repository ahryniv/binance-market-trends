from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
Base = declarative_base(metadata=metadata)
CookieCutterSession = sessionmaker(autocommit=False, autoflush=False)


def get_db():
    session = CookieCutterSession()
    try:
        yield session
    finally:
        session.close()
