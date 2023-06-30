## Run a vector store agent over multiple vector stores
## The intent here would be to use OpenAI's LLM to route requests to the proper chain
## and then have the chains associated with the different vector stores use their own LLMs
## e.g. a publicly available set of documents is used with the OpenAI LLM and private docs use a local LLM

from selector import get_llm, get_embedding
import argparse
import shared
import time
import utilities.console_text as console_text
import shared
import utilities.calculate_timing as calculate_timing
from langchain.memory import ConversationTokenBufferMemory, ReadOnlySharedMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from tool_loader import load_tools_from_file

def main(router_llm, configuration_file, verbose, max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE):  
    
    memory = ConversationTokenBufferMemory(llm=router_llm, max_token_limit=max_tokens, memory_key="chat_history", return_messages=True)   

    # Share my memory with all my buds
    tools = load_tools_from_file(configuration_file, memory)
    
    agent_chain = initialize_agent(tools, router_llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=verbose, memory=memory)

    while True:
        query = input("Query (x to exit): ")

        if query == "x":
            exit()

        if len(memory.buffer) == 0:
            query = "Without using knowledge prior to this conversation, and using one or more of the tools available to you, respond to the following: " + query             

        # Time it
        start_time = time.time()       

        # Run the query
        result = agent_chain.run(input=query)

        end_time = time.time()

        # print the answer
        console_text.print_green(result)        
        
        elapsed_time = end_time - start_time

        print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))



def run(run_local:bool, verbose:bool, configuration_file:str):    
    print("-------- Running LLM --------")
    print("run_local:", run_local)
    print("verbose:", verbose)
    print("configuration_file:", configuration_file)
    print("-----------------------------")
    
    if run_local:    
        llm = get_llm(True)
        max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE
    else:
        llm = get_llm(False)
        max_tokens = shared.MAX_OPEN_AI_CONTEXT_SIZE
        
    main(llm, configuration_file, verbose, max_tokens)
      
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--run_open_ai', action='store_true', default=False, help='Use OpenAI vs. local LLM')
parser.add_argument('--verbose', action='store_true', default=False, help='Verbose mode')
parser.add_argument('--config', type=str, required=True, help='Path to the tools configuration file')

# Parse the command-line arguments
args = parser.parse_args()

# Call the run() method with parsed arguments
run(run_local=args.run_open_ai == False, verbose=args.verbose, configuration_file=args.config)