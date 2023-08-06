from pydantic import BaseModel

class TestModel(BaseModel):
    id: int
    name: str