## Where I'm keeping a bunch of different chain types / llms to experiment with

import os
from langchain.llms import (OpenAI, LlamaCpp)
from langchain.embeddings import (OpenAIEmbeddings, HuggingFaceInstructEmbeddings)

from shared import (LOCAL_MODEL_PATH)

def get_llm(local_llm):
    if local_llm:  
        ## Ignore the context size
        return LlamaCpp(model_path=LOCAL_MODEL_PATH, n_ctx=40960, temperature=0, n_gpu_layers=40) 
    else:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        return OpenAI(temperature=0, openai_api_key=openai_api_key)
    
def get_embedding(local):
    if local:
        return HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") #, embed_instruction="Represent the document for retrieval: ")
    else:
        return OpenAIEmbeddings()    