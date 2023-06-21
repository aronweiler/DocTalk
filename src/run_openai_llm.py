import os
import time
import utilities.console_text as console_text
from selector import get_llm
import documents
import utilities.calculate_timing as timing
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


def main(top_k = 4, verbose = False):       
    # Get the openai llm and embeddings
    llm = get_llm(False)
    db = documents.get_database(False)

    # These arguments might not be supported on the Chroma db- need to investigate
    # Looks like they are not right now- might need to use a different vectorstore
    # Actually, looks like this is supported, it just needs to be put into the as_retriever call
    vectordbkwargs = {"search_distance": 0.9, "k": top_k}

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="question", output_key="answer")
    qa = ConversationalRetrievalChain.from_llm(llm, db.as_retriever(search_kwargs=vectordbkwargs), memory=memory, verbose=verbose, return_source_documents=True)

    while True:        
        query = input("Query (x to exit): ")

        if query == "x":
            exit()

        # Time it
        start_time = time.time()
        
        # Run the query
        result = qa({"question": query, "vectordbkwargs": vectordbkwargs})

        end_time = time.time()

        # print the answer
        console_text.print_green(result['answer'])
        source_docs = "\n".join([f"\t- {os.path.basename(d.metadata['source'])} page {d.metadata['page']}" for d in result["source_documents"]])
        console_text.print_blue("Source documents:\n" + source_docs)
        
        elapsed_time = end_time - start_time

        print("Operation took: ", timing.convert_milliseconds_to_english(elapsed_time * 1000))

