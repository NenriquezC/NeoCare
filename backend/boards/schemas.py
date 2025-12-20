from pydantic import BaseModel

class BoardBase(BaseModel):
    title: str

class BoardOut(BoardBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
