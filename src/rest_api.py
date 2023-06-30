import os
from fastapi import FastAPI
from run_chain import get_llm, get_embedding
import shared
from pydantic import BaseModel
from typing import List
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import Tool
from tools.vector_store_retrieval_qa_tool import VectorStoreRetrievalQATool
from tool_loader import load_tools_from_file

app = FastAPI()

@app.get("/query/{query}")
def read_item(query: str):
    print(query)
    return {"result": agent_chain.run(input=query)}

# Add arguments from environment vars
run_open_ai = os.environ.get("run_open_ai", False)
database_name = os.environ.get("database_name", None)
verbose = os.environ.get("verbose", True)
top_k = os.environ.get("top_k", 4)
search_distance = os.environ.get("search_distance", 0.1)
search_type = os.environ.get("search_type", "similarity")
chain_type = os.environ.get("chain_type", "stuff")
configuration_file = os.environ.get("configuration_file", None)



if run_open_ai:    
    router_llm = get_llm(False)
    embeddings = get_embedding(False)
    max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE
else:
    router_llm = get_llm(True)
    embeddings = get_embedding(True)
    max_tokens = shared.MAX_OPEN_AI_CONTEXT_SIZE

memory = None

local_llm = get_llm(True)

tools = load_tools_from_file(configuration_file, memory, local_llm)

agent_chain = initialize_agent(tools=tools, llm=router_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=verbose)


#input("Press any key to exit")