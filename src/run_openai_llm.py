import os
import time
import utilities.console_text as console_text
from selector import get_llm

import documents
from utilities.token_helper import num_tokens_from_string
import utilities.calculate_timing as calculate_timing
import shared

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

from langchain.memory import ConversationBufferMemory
from query_parser import parse_query


def main(verbose = False):   
    
    # Get the openai llm and embeddings
    llm = get_llm(False)
    db = documents.get_database(False)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, db.as_retriever(), memory=memory, verbose=verbose)

    while True:        
        query = input("Query (x to exit): ")

        if query == "x":
            exit()

        # Time it
        start_time = time.time()
        
        # Run the query
        result = qa({"question": query})

        end_time = time.time()

        # print the answer
        console_text.print_green(result['answer'])        
        
        elapsed_time = end_time - start_time

        print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))

