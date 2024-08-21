from main.agent.graph.graph import graph
from langchain_core.messages import HumanMessage


def agent_runner():
    print("---STARTING THE AGENT RUNNER---")
    inputs = {
        "json_query": "test",
        "file_path": "main/test_5g/"
    }
    result = graph.invoke(inputs)
    return result["result"], result["generated_query"]


