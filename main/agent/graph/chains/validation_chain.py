# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
# from main.agent.graph.chains.prompts.agents_prompts import prompt_template_validate
#
#
# def create_validate_agent():
#     model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
#     parser = StrOutputParser()
#     validate_chain = prompt_template_validate | model | parser
#     return validate_chain
