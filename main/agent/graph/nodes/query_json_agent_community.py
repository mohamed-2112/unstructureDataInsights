from typing import Any, Dict
from langchain_community.agent_toolkits import JsonToolkit
from main.agent.graph.state import GraphState
from langchain_core.messages import AIMessage
from langchain_community.tools.json.tool import JsonSpec
from langchain.agents.agent_types import AgentType
from main.agent.graph.chains.community_agent_chain import create_pandas_agent_with_df

def query_json(state) -> Dict[str, Any]:
    """
    Query the json file based on the user request.
    :param state:
    :return:
    """
    print("---QUERY---")
    #json_spec = JsonSpec(dict_=state["json_data"], max_value_length=4000)
    #json_agent.tools[0].spec = json_spec
    #json_agent.tools[1].spec = json_spec
    #response = json_agent.invoke({"input": state["json_query"]})
    print(state["json_data"].columns)
    agent = create_pandas_agent_with_df(df=state["json_data"])
    result = agent.invoke(state["json_query"])
    state["result"] = state['columns_names']
    print(state["result"])
    return state
