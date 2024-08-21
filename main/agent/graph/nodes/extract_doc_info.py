from typing import Any, Dict
from main.agent.graph.state import GraphState


def extract_doc_info_node(state: GraphState) -> Dict[str, Any]:
    """
    Validate whether the result from query of on the json file align with the request of the user or not.
    :param state:
    :return:
    """
    print("---EXTRACT DOC INFO---")
    return state
