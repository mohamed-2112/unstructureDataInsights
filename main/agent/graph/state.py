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
    valid_result: str
    file_path: str
