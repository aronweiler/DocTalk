import os
import time
import utilities.console_text as console_text
import utilities.calculate_timing as calculate_timing
from ai.abstract_ai import AbstractAI
from runners.runner import Runner

class ConsoleRunner(Runner):
    def __init__(self):
        super().__init__()
        

    def run(self, abstract_ai: AbstractAI):
        while True:        
            query = input("Query (x to exit): ")

            if query == "x":
                exit()

            # Time it
            start_time = time.time()
                    
            # Run the query
            result = abstract_ai.query(query)

            end_time = time.time()

            # print the answer
            console_text.print_green(result.result)
            source_docs = "\n".join([f"\t-{doc['document']} - Page {doc['page']}" for doc in result.source_documents])
            console_text.print_blue("Source documents:\n" + source_docs)
            
            elapsed_time = end_time - start_time

            print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))