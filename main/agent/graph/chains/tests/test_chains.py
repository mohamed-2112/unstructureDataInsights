from dotenv import load_dotenv

load_dotenv("D:\PycharmProjects\jsonAgent\config\.env")
from pprint import pprint
from main.agent.graph.chains.pandas_dataframe_chain import create_react_agent

def test_generation_chain() -> None:
    question = "give the query that get me all the names"
    agent = create_react_agent()
    result = agent.invoke({"coulmns_names": "[name, age]", "query": question})
    pprint(result)

