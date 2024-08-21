from langgraph.graph import StateGraph, START, END
from main.agent.graph.state import GraphState
#from constants.consts import LOAD_JSON, QUERY, VALIDATE
from langchain_core.runnables import RunnablePassthrough
from main.agent.graph.nodes import (
    validate_node,
    search_insight_node,
    save_insight_node,
    re_search_doc_node,
    extract_insight_node,
    feed_back_node,
    extract_doc_info_node)

EXTRACT_DOC_INFO = "extract_doc_info"
EXTRACT_INSIGHT = "extract_insight"
FEED_BACK = "feed_back"
RE_SEARCH_DOC = "re_search_doc"
SAVE_INSIGHT = "save_insight"
SEARCH_INSIGHT = "search_insight"
VALIDATE = "validate"


def insight_search_result_cond(state: GraphState):
    validation_value = state["valid_result"]
    if "not found" in validation_value:
        return RE_SEARCH_DOC
    else:
        return FEED_BACK


def feed_back_result_cond(state: GraphState):
    validation_value = state["valid_result"]
    if "not found" in validation_value:
        return EXTRACT_DOC_INFO
    else:
        print("---END---")
        return "end"


def doc_search_result_cond(state: GraphState):
    validation_value = state["valid_result"]
    if "not found" in validation_value:
        return FEED_BACK
    else:
        return SEARCH_INSIGHT


# Init graph
graph_builder = StateGraph(GraphState)

# Init nodes
graph_builder.add_node(EXTRACT_DOC_INFO, extract_doc_info_node)
graph_builder.add_node(EXTRACT_INSIGHT, extract_insight_node)
graph_builder.add_node(SAVE_INSIGHT, save_insight_node)
graph_builder.add_node(SEARCH_INSIGHT, search_insight_node)
graph_builder.add_node(FEED_BACK, feed_back_node)
graph_builder.add_node(RE_SEARCH_DOC, re_search_doc_node)

# Add Edges
graph_builder.set_entry_point(EXTRACT_DOC_INFO)
graph_builder.add_edge(EXTRACT_DOC_INFO, EXTRACT_INSIGHT)
graph_builder.add_edge(EXTRACT_INSIGHT, SAVE_INSIGHT)
graph_builder.add_edge(SAVE_INSIGHT, SEARCH_INSIGHT)


graph_builder.add_conditional_edges(
    SEARCH_INSIGHT,
    insight_search_result_cond,
    {
        "re_search_doc": RE_SEARCH_DOC,
        "feed_back": FEED_BACK
    }
)

graph_builder.add_conditional_edges(
    FEED_BACK,
    feed_back_result_cond,
    {
        "extract_doc_info": EXTRACT_DOC_INFO,
        "end": END
    }
)

graph_builder.add_conditional_edges(
    RE_SEARCH_DOC,
    doc_search_result_cond,
    {
        "feed_back": FEED_BACK,
        "search_insight": SEARCH_INSIGHT
    }
)

# compile graph
graph = graph_builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="resources/graph.png")
