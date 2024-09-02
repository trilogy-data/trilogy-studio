from typing import Any, List, Union

from trilogy.core.models import (
    AggregateWrapper,
    Comparison,
    Concept,
    Conditional,
    FilterItem,
    Function,
    WindowItem,
    Environment,
    DataType,
    RowsetItem,
    SelectStatement,
    MultiSelectStatement,
    MergeStatementV2,
)

from backend.io_models import LineageItem, Model, UIConcept
from trilogy.constants import DEFAULT_NAMESPACE
from trilogy.parsing.render import Renderer


def flatten_array(input: Any, depth: int = 0) -> List[LineageItem]:
    arr_len = len(input)
    output = []
    for idx, val in enumerate(input):
        output += flatten_lineage(val, depth)
        if idx < arr_len - 1:
            output.append(LineageItem(token=",", depth=depth - 1))
    return output


def flatten_lineage(
    input: Union[
        Concept,
        int,
        float,
        str,
        DataType,
        Function,
        WindowItem,
        FilterItem,
        Conditional,
        Comparison,
        AggregateWrapper,
        RowsetItem,
        MultiSelectStatement,
        MergeStatementV2,
        SelectStatement,
    ],
    depth: int = 0,
) -> List[LineageItem]:
    if depth == 0:
        chain = []
    elif isinstance(input, Function):
        chain = [
            LineageItem(token=input.operator.name, depth=depth),
            LineageItem(token="(", depth=depth),
        ]  # ], ')']
        chain += flatten_array(input.arguments, depth + 1)
        chain += [LineageItem(token=")", depth=depth)]
    elif isinstance(input, WindowItem):
        chain = [
            LineageItem(token="rank", depth=depth),
            LineageItem(token="(", depth=depth),
        ]  # ], ')']
        chain += flatten_lineage(input.content, depth + 1)
        chain += [LineageItem(token="over", depth=depth)]
        chain += flatten_array(input.over, depth + 1)
        chain += [LineageItem(token="order by", depth=depth)]
        chain += flatten_array(input.order_by, depth + 1)
        chain += [LineageItem(token=")", depth=depth)]
    elif isinstance(input, FilterItem):
        chain = [
            LineageItem(token="filter", depth=depth),
            LineageItem(token="(", depth=depth),
        ]  # ], ')']
        chain += flatten_lineage(input.content, depth + 1)
        chain += [LineageItem(token="by", depth=depth)]
        chain += flatten_array(input.where.input, depth + 1)
        chain += [LineageItem(token=")", depth=depth)]
    elif isinstance(input, AggregateWrapper):
        return flatten_lineage(input.function, depth)
    elif isinstance(input, RowsetItem):
        chain = []
        chain += [LineageItem(token="(", depth=depth)]
        chain += [LineageItem(token=input.rowset.name, depth=depth)]
        chain += [LineageItem(token=")", depth=depth)]
    elif isinstance(input, SelectStatement):
        chain = []
        chain += [LineageItem(token="(", depth=depth)]
        chain += [LineageItem(token="CTE", depth=depth)]
        chain += flatten_array(input.output_components, depth + 1)
        chain += [LineageItem(token=")", depth=depth)]
    elif isinstance(input, MergeStatementV2):
        chain = []
        chain += [LineageItem(token="(", depth=depth)]
        chain += [LineageItem(token="MERGE", depth=depth)]
        chain += flatten_array(input.target, depth + 1)
        chain += [LineageItem(token=")", depth=depth)]
    elif isinstance(input, MultiSelectStatement):
        chain = []
        chain += [LineageItem(token="(", depth=depth)]
        chain += [LineageItem(token="MULTISELECT", depth=depth)]
        for select in input.selects:
            chain += flatten_lineage(select, depth + 1)
        chain += [LineageItem(token=")", depth=depth)]
    elif not isinstance(input, Concept):
        return [LineageItem(token=str(input), depth=depth)]
    else:
        chain = [LineageItem(token=input.address, depth=depth)]

    # enrich block
    if isinstance(input, Concept) and input.lineage:
        if not depth == 0:
            chain += [LineageItem(token="<-", depth=depth)]
        chain += flatten_lineage(input.lineage, depth + 1)

    return chain


def model_to_response(
    name: str, env: Environment, render_to_text: bool = False
) -> Model:
    final_concepts = []
    rendered = Renderer().to_string(env) if render_to_text else None
    for skey, sconcept in env.concepts.items():
        # don't show private concepts
        if sconcept.name.startswith("_"):
            continue
        final_concepts.append(
            UIConcept(
                name=(
                    sconcept.name.split(".")[-1]
                    if sconcept.namespace == DEFAULT_NAMESPACE
                    else sconcept.name
                ),
                datatype=sconcept.datatype,
                purpose=sconcept.purpose,
                description=(
                    sconcept.metadata.description if sconcept.metadata else None
                ),
                namespace=sconcept.namespace or "",
                key=skey,
                lineage=flatten_lineage(sconcept, depth=0),
            )
        )
    final_concepts.sort(key=lambda x: x.namespace + x.key)
    return Model(name=name, concepts=final_concepts, rendered=rendered)
