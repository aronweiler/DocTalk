import os
import time
import utilities.console_text as console_text
import documents
import shared
import utilities.calculate_timing as calculate_timing
import callback_handlers
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationTokenBufferMemory

def main(llm, embeddings, database_name:str, top_k = 4, search_distance = .5, verbose = False, max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE):  
    db = documents.get_database(embeddings, database_name) 
    
    vectordbkwargs = {"search_distance": search_distance, "k": top_k, "search_type": "similarity"}

    memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=max_tokens, memory_key="chat_history", return_messages=True, input_key="question", output_key="answer")    
    qa = ConversationalRetrievalChain.from_llm(llm, db.as_retriever(search_kwargs=vectordbkwargs), memory=memory, verbose=verbose, return_source_documents=True, callbacks=[callback_handlers.DebugCallbackHandler()])

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
        source_docs = "\n".join([f"\t- {os.path.basename(d.metadata['source'])} page {d.metadata['page']}" if 'page' in d.metadata else f"\t- {os.path.basename(d.metadata['source'])}" for d in result["source_documents"]])
        console_text.print_blue("Source documents:\n" + source_docs)
        
        elapsed_time = end_time - start_time

        print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))

