from main.agent.graph.graph import graph
from langchain_core.messages import HumanMessage


def agent_runner():
    print("---STARTING THE AGENT RUNNER---")
    inputs = {
        "valid_result": "found",
        "file_path": "main/test_5g/"
    }
    graph.invoke(inputs)


