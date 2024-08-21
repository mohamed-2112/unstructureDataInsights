from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate

JSON_PROMPT_PREFIX = """
First set the pandas display options to show all the columns,
get the column names, then answer the question.
"""

JSON_PROMPT_SUFFIX = """
- **IMPORTANT**: Do not load or access any data from the DataFrame. Only use the column names to address your query. This means you should not perform any operations that involve loading data or accessing the data itself.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got to the answer in a section that starts with:
  \n\nExplanation:\n
  In the explanation, mention the column names that you used to get to the final answer.
"""


system_template_react = """You are a Data Engineer expert with extensive experience in working with pandas DataFrames.
Your task is to generate queries on the DataFrame using only the provided column names. {coulmns_names}
Ensure that your queries are accurate, efficient, and adhere to best practices in pandas.The name of the dataframe is alawys df. Generate only a panadas dataframe query and return it into a json and here is an example on how should you return the json "query": "df[host.brand].unique()" """

prompt_template_react = ChatPromptTemplate.from_messages([("system", system_template_react), ("user", "{query}")])


template_validate = """You are a Data Engineer expert with extensive experience in working with pandas DataFrames queries.
Your task is to validate queries and ONLY TO VALIDATE on the DataFrame query that will be provided using only the 
provided column names. 
Ensure that your validations are accurate.The name of the dataframe is always df.
return the mistake that should be modified, if the query is valid then return only the word "valid" and nothing else.
columns names: {columns_names}
query: {query}
"""

prompt_template_validate = PromptTemplate(input_variables=["columns_names", "query"], template=template_validate)


from langchain_core.prompts import ChatPromptTemplate

fix_dataframe_system_template = """
You are a highly skilled Data Engineer with extensive expertise in manipulating pandas DataFrames. Your task is to analyze and fix any issues in the provided pandas DataFrame query and then to generate efficient and accurate pandas DataFrame queries using only the provided column names: {column_names}. The DataFrame is always named 'df'.The user ask about {query} and the generated dataframe query is : {generated_query} and the exception: {exception} when trying to run it. Your output should be a corrected pandas query, strictly following pandas best practices and returning the corrected query formatted as a JSON object, with the key 'query'. If the original query is correct, confirm its correctness. The output should look like this: {{"query": "df['column_name'].unique()"}}. Ensure the query is optimized for performance and readability.

Here are 5 examples to guide your responses:

1. Gener: "What is the average age?"
   Query: {{"query": "df['age'].mean()"}}

2. Input: "How many times does each city appear?"
   Query: {{"query": "df['city'].value_counts()"}}

3. Input: "What is the total profit?"
   Query: {{"query": "df['profit'].sum()"}}

4. Input: "What is the highest temperature recorded?"
   Query: {{"query": "df['temperature'].max()"}}

5. Input: "Remove duplicate products and their prices."
   Query: {{"query": "df[['product', 'price']].drop_duplicates()"}}

Now, analyze and correct the generated query: 
"""

fix_pandas_dataframe_prompt_template = ChatPromptTemplate.from_messages([("system", fix_dataframe_system_template)])
