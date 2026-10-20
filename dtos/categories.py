
from pydantic import BaseModel, ConfigDict, Field


class CategoryDto(BaseModel):
    # from_attributes sallii luonnin suoraan SQLAlchemy-oliosta
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CreateCategoryReq(BaseModel):
    name: str = Field(min_length=2, max_length=50)