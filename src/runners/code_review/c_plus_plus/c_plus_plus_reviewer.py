import os
import time
from datetime import datetime
from typing import List
from runners.code_review.c_plus_plus.function_splitter import CSplitter
from runners.code_review.c_plus_plus.prompts import GENERATED_PROMPTS

class CPlusPlusReviewer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_extension = os.path.splitext(self.file_name)[1]
        self.file_name_without_extension = os.path.splitext(self.file_name)[0]

        self.cspliter = CSplitter()

    def review(self, abstract_ai) -> List[str]:
        # Temp function to test the AI
        # Read in the code file
        with open(self.file_path, 'r') as file:
            code = file.read()

        output_texts = []
        # Run the code through the AI
        for prompt in GENERATED_PROMPTS:
            p = prompt.format(code=code, language="C++")
            #output_markdown = "tesst"
            output_markdown = abstract_ai.query(p).result_string
            output_texts.append(output_markdown)

            # Write the prompt and output_markdown to a file named with the date and time
            # create the file name:
            temp_file_name = f"code_review-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.md"
            temp_file_path = os.path.join("c:\\temp\\code_review", temp_file_name)
            with open(temp_file_path, "w") as file:
                file.write(p)
                file.write("\n\n")
                file.write(output_markdown)
            
            time.sleep(2) 

            # Write the file to c:\temp


        ## Here is code to use when splitting the C++ file up - use this when the AI is ready
        # ---------------------------------------------------------------------------------------------
        # Split the file into functions
        # code_chunks = self.cspliter.parse_cpp_file(self.file_path)

        # # Run the functions through the AI.  The AI will return a list of markdown strings
        # results = []
        # for chunk in code_chunks:            
        #     results.append(abstract_ai.query(REVIEW_FOR_BUFFER_OVERFLOW_PROMPT.format(code=chunk, language="C++")).result_string)

        # Combine the markdown strings into a single string
        # output_text = ""
        # for result in results:
        #     output_text += result
        # ---------------------------------------------------------------------------------------------

        return output_texts

