from pydantic import BaseModel


class PairBase(BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True


class Pair(PairBase):
    id: int
