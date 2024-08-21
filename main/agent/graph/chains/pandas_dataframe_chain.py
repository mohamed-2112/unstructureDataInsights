from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from main.agent.graph.chains.prompts.pandas_dataframe_prompts import pandas_dataframe_prompt_template


def create_data_frame_chain():
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    parser = StrOutputParser()
    react_chain = pandas_dataframe_prompt_template | model | parser
    return react_chain
