from typing import TypedDict, Annotated, Sequence
import operator
from typing import TypedDict, Annotated, Union
import operator
from langchain_core.messages import BaseMessage
import pandas as pd

class GraphState(TypedDict):
    """
    Represents the state of a graph.
    Attributes:
    """
    columns_names: list
    json_data: pd.DataFrame
    generated_query: str
    json_query: str
    result: Union[dict, None]
    valid_result: str
    file_path: str
