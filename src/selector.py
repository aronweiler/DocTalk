import os
from langchain.llms import (OpenAI, LlamaCpp)
from langchain.embeddings import (OpenAIEmbeddings, HuggingFaceInstructEmbeddings)

import shared

def get_llm(local):
    if local:  
        return LlamaCpp(model_path=shared.LOCAL_MODEL_PATH, n_ctx=shared.MAX_LOCAL_CONTEXT_SIZE, temperature=shared.AI_TEMP, n_gpu_layers=shared.OFFLOAD_TO_GPU_LAYERS) 
    else:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        return OpenAI(temperature=shared.AI_TEMP, openai_api_key=openai_api_key)
    
def get_embedding(local):
    
    if local:
        return HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") #, embed_instruction="Represent the document for retrieval: ")
    else:
        return OpenAIEmbeddings()  