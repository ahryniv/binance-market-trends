from pydantic import BaseModel


class OKSchema(BaseModel):
    OK: str = 'OK'
