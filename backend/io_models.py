from typing import List, Optional, Dict, Tuple

from trilogy.core.models import (
    DataType,
    Purpose,
    ListType,
    MapType,
    StructType,
    NumericType,
)
from pydantic import BaseModel, Field
from trilogy_nlp.enums import Provider
from trilogy import Dialects
from datetime import datetime


class LineageItem(BaseModel):
    token: str
    depth: int
    link: str | None = None


class UIConcept(BaseModel):
    key: str
    name: str
    namespace: str
    datatype: DataType | ListType | MapType | StructType | NumericType
    purpose: Purpose
    description: Optional[str] = None
    lineage: List[LineageItem] = Field(default_factory=list)


class Model(BaseModel):
    name: str
    concepts: List[UIConcept]
    rendered: str | None = None


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
    genai_connection: str


class GenAIQueryOutSchema(BaseModel):
    text: str


class FormatQueryOutSchema(BaseModel):
    text: str


class InputRequest(BaseModel):
    text: str
    connection: str
    # conversation:str


class ModelSourceInSchema(BaseModel):
    alias: str
    contents: str


class ModelInSchema(BaseModel):
    name: str
    sources: List[ModelSourceInSchema]


class ConnectionInSchema(BaseModel):
    name: str
    dialect: Dialects
    extra: Dict | None = Field(default_factory=dict)
    model: str | None = None
    full_model: ModelInSchema | None = None


class ConnectionListItem(BaseModel):
    name: str
    dialect: Dialects
    model: str


class ConnectionListOutput(BaseModel):
    connections: List[ConnectionListItem]


class QueryOutColumn(BaseModel):
    name: str
    datatype: DataType
    purpose: Purpose


class QueryOut(BaseModel):
    connection: str
    query: str
    generated_sql: str
    headers: list[str]
    results: list[dict]
    created_at: datetime = Field(default_factory=datetime.now)
    refreshed_at: datetime = Field(default_factory=datetime.now)
    duration: Optional[int]
    columns: List[Tuple[str, QueryOutColumn]] | None
