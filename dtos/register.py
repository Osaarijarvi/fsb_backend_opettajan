
from pydantic import BaseModel, ConfigDict, Field


class RegisterReq(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class RegisterRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str