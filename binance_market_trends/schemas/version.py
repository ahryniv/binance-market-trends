from pydantic.main import BaseModel


class VersionSchema(BaseModel):
    version: str
