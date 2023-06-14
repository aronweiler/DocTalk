## Where I'm keeping a bunch of different chain types to experiment with

import os
from langchain.llms import (OpenAI, LlamaCpp)

from shared import (RUN_LOCAL, LOCAL_MODEL_PATH)

def get_llm():
    if RUN_LOCAL:  
        ## Ignore the context size
        return LlamaCpp(model_path=LOCAL_MODEL_PATH, n_ctx=40960, temperature=0, n_gpu_layers=40) 
    else:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        return OpenAI(temperature=0, openai_api_key=openai_api_key)