import logging
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
            # Get the query, which can be multiple lines            
            logging.debug("Query (Enter twice to run, X to exit):")
            
            query = self.get_multi_line_console_input()


            if query == "x":
                exit()

            # Time it
            start_time = time.time()
                    
            # Run the query
            result = abstract_ai.query(query)

            end_time = time.time()

            # print the answer
            console_text.print_green(result.result_string)            
            source_docs = self.get_source_docs_to_logging.debug(result.source_documents)
            console_text.print_blue("Source documents:\n" + source_docs)
            
            elapsed_time = end_time - start_time

            logging.debug("Operation took: " + calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))

    def get_multi_line_console_input(self):
        # Get the query, which can be multiple lines, until the user presses enter twice
        query = ""
        while True:
            line = input()
            if line == "":
                break
            query += line + "\n"

        return query