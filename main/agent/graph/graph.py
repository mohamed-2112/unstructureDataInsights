from langgraph.graph import StateGraph, START, END
from main.agent.graph.state import GraphState
#from constants.consts import LOAD_JSON, QUERY, VALIDATE
from main.agent.graph.nodes import load_json, query_json, validate_node, query_json_dataframe_chain, query_dataframe, fix_dataframe_query
from langchain_core.runnables import RunnablePassthrough

QUERY = "query"
VALIDATION = "validation"
LOAD_JSON = "load_json"
RUN = "run"


def validation_condition(state: GraphState):
    validation_value = state["valid_result"]
    if "valid" in validation_value:
        return RUN
    else:
        return QUERY
    
def check_error(state: GraphState):
    print("tttttttttttttttttttttttttttttt")
    result = state["result"]
    if "error" in result or "Error" in result:
        print("tttttttttttttttttttttttttttttt1=",result,"//Generated Query=",state["generated_query"])
        return "fix_error"
    else:
        print("tttttttttttttttttttttttttttttt2")
        return "end"


# Init graph
graph_builder = StateGraph(GraphState)

# Init nodes
graph_builder.add_node(LOAD_JSON, load_json)
graph_builder.add_node(QUERY, query_json_dataframe_chain)
graph_builder.add_node("run", query_dataframe)
graph_builder.add_node(VALIDATION, validate_node)
graph_builder.add_node("check_error", RunnablePassthrough())
graph_builder.add_node("fix_query", fix_dataframe_query)

# Add Edges
graph_builder.set_entry_point(LOAD_JSON)
graph_builder.add_edge(LOAD_JSON, QUERY)
graph_builder.add_edge(QUERY, VALIDATION)
graph_builder.add_conditional_edges(
    VALIDATION,
    validation_condition,
    {
        "run": RUN,
        "query": QUERY
    }
)
graph_builder.add_edge(RUN, "check_error")
graph_builder.add_conditional_edges(
    "check_error",
    check_error,
    {
        "fix_error": "fix_query",
        "end" : END
    }
)
graph_builder.add_edge("fix_query", RUN)


# compile graph
graph = graph_builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph_3.png")
