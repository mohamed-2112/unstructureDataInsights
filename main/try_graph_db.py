from langchain_community.graphs import Neo4jGraph

graph = Neo4jGraph()

# Import movie information
movies_query = """
LOAD CSV WITH HEADERS FROM 
'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv'
AS row
MERGE (m:Movie {id:row.movieId})
SET m.released = date(row.released),
    m.title = row.title,
    m.imdbRating = toFloat(row.imdbRating)
FOREACH (director in split(row.director, '|') | 
    MERGE (p:Person {name:trim(director)})
    MERGE (p)-[:DIRECTED]->(m))
FOREACH (actor in split(row.actors, '|') | 
    MERGE (p:Person {name:trim(actor)})
    MERGE (p)-[:ACTED_IN]->(m))
FOREACH (genre in split(row.genres, '|') | 
    MERGE (g:Genre {name:trim(genre)})
    MERGE (m)-[:IN_GENRE]->(g))
"""

graph.query(movies_query)

match_query_2 = """MATCH (p:Person|Movie)
WHERE p.name CONTAINS $value OR p.title CONTAINS $value
RETURN coalesce(p.name, p.title) AS result, labels(p)[0] AS type
LIMIT 1
"""
print("EE")
response = graph.query(match_query_2, {"value": "casino"})
print("EEE",response)

from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class Entities(BaseModel):
    """Identifying information about entities."""
    names: List[str] = Field(...,description="All the person or movies appearing in the text",)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are extracting person and movies from the text.",
        ),
        (
            "human",
            "Use the given format to extract information from the following "
            "input: {question}",
        ),
    ]
)


entity_chain = prompt | llm.with_structured_output(Entities)
entities = entity_chain.invoke({"question": "Who played in Casino movie?"})
print(entities)

match_query = """MATCH (p:Person|Movie)
WHERE p.name CONTAINS $value OR p.title CONTAINS $value
RETURN coalesce(p.name, p.title) AS result, labels(p)[0] AS type
LIMIT 1
"""


"""
def map_to_database(entities: Entities) -> Optional[str]:
    result = ""
    for entity in entities.names:
        print("entity:",entity)
        response = graph.query(match_query, {"value": entity})
        print("response:",response)
        result += f"{entity} maps to {response[0]['result']} {response[0]['type']} in database\n"
    return result
"""

def map_to_database(entities: Entities) -> Optional[str]:
    result = ""
    for entity in entities.names:
        response = graph.query(match_query, {"value": entity})
        try:
            result += f"{entity} maps to {response[0]['result']} {response[0]['type']} in database\n"
        except IndexError:
            pass
    return result


res = map_to_database(entities)
print(res)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Generate Cypher statement based on natural language input
cypher_template = """Based on the Neo4j graph schema below, write a Cypher query that would answer the user's question:
{schema}
Entities in the question map to the following database values:
{entities_list}
Question: {question}
Cypher query:"""

cypher_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question, convert it to a Cypher query. No pre-amble.",
        ),
        ("human", cypher_template),
    ]
)

cypher_response = (
    RunnablePassthrough.assign(names=entity_chain)
    | RunnablePassthrough.assign(
        entities_list=lambda x: map_to_database(x["names"]),
        schema=lambda _: graph.get_schema,
    )
    | cypher_prompt
    | llm.bind(stop=["\nCypherResult:"])
    | StrOutputParser()
)

cypher = cypher_response.invoke({"question": "Who played in Casino movie?"})
print(cypher)