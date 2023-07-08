from typing import List, Optional

from preql.core.models import DataType, Purpose
from pydantic import BaseModel, Field


class LineageItem(BaseModel):
    token: str
    depth: int
    link: str | None = None


class UIConcept(BaseModel):
    key: str
    name: str
    namespace: str
    datatype: DataType
    purpose: Purpose
    description: Optional[str] = None
    lineage: List[LineageItem] = Field(default_factory=list)


class Model(BaseModel):
    name: str
    concepts: List[UIConcept]


class ListModelResponse(BaseModel):
    models: List[Model]
