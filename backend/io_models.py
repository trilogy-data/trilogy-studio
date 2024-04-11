from typing import List, Optional, Dict

from preql.core.models import DataType, Purpose
from pydantic import BaseModel, Field
from preql_nlp.enums import Provider


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


class GenAIConnectionInSchema(BaseModel):
    name: str
    provider: Provider
    api_key: str = Field(alias="apiKey")
    extra: Dict = Field(default_factory=dict)

class QueryInSchema(BaseModel):
    connection: str
    query: str
    # chart_type: ChartType | None = None

class GenAIQueryInSchema(BaseModel):
    connection: str
    text: str
    genai_connection:str

class GenAIQueryOutSchema(BaseModel):
    text:str