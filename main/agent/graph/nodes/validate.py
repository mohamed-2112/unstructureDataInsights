from typing import Any, Dict
from main.agent.graph.state import GraphState
from langchain_core.messages import AIMessage
from main.agent.graph.chains.validation_chain import create_validate_agent


def validate_node(state: GraphState) -> Dict[str, Any]:
    """
    Validate whether the result from query of on the json file align with the request of the user or not.
    :param state:
    :return:
    """
    print("---VALIDATE---")
    print("the status now is: ")
    # validate
    validate_agent = create_validate_agent()
    validation_result = validate_agent.invoke({"columns_names": state["columns_names"], "query": state["result"]})
    state["valid_result"] = validation_result
    print(state["valid_result"])
    return state
