import os
from langchain.llms import (OpenAI, LlamaCpp)
from langchain.embeddings import (OpenAIEmbeddings, HuggingFaceInstructEmbeddings)

import shared.constants as constants

def get_llm(local, ai_temp = constants.AI_TEMP):
    if local:          
        
        if os.environ.get("OFFLOAD_TO_GPU_LAYERS") == None: 
            offload_layers = constants.OFFLOAD_TO_GPU_LAYERS
        else:
            offload_layers = os.environ.get("OFFLOAD_TO_GPU_LAYERS")

        return LlamaCpp(model_path=constants.LOCAL_MODEL_PATH, n_ctx=constants.MAX_LOCAL_CONTEXT_SIZE, temperature=ai_temp, n_gpu_layers=offload_layers) 
    else:
        openai_api_key = get_openai_api_key()
        return OpenAI(temperature=ai_temp, openai_api_key=openai_api_key)#, max_tokens=-1)
    
def get_embedding(local, device_type = "cpu"):    
    if local:
        return HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs={"device": device_type}) #, embed_instruction="Represent the document for retrieval: ")
    else:
        openai_api_key = get_openai_api_key()
        return OpenAIEmbeddings(openai_api_key=openai_api_key)  
    
def get_openai_api_key():
    from dotenv import dotenv_values, load_dotenv
    load_dotenv()
    return dotenv_values().get('OPENAI_API_KEY')