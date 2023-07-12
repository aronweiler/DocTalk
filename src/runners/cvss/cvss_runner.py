import os
import io
import re
from ai.abstract_ai import AbstractAI
from runners.runner import Runner
from runners.cvss.prompts import  CVSS_INSTRUCT_PROMPT, CHAIN_OF_THOUGHT_EXAMPLE_DATA_1, CHAIN_OF_THOUGHT_EXAMPLE_DATA_2, CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1, CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2

from utilities.token_helper import num_tokens_from_string

from cvss import CVSS3

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

class CvssRunner(Runner):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self, abstract_ai: AbstractAI):

        input_dir = self.args["input_directory"]
        output_dir = self.args["output_directory"]
        all_files = os.listdir(input_dir)        

        for file_path in all_files:
            input_file_path = os.path.join(input_dir, file_path)

            if not os.path.isfile(input_file_path):
                continue

            # Create the output file path by appending _analysis to the input file path before the extension
            output_file_path = os.path.join(output_dir, file_path[:file_path.rfind('.')] + '_analysis' + file_path[file_path.rfind('.'):])

            with io.open(input_file_path, "r", encoding="utf-8") as input_file:
                input_file_data = input_file.read()

            # Note: we should consider pulling out all of the CVSS relevant data from the input file first- 
            # Sometimes the input file has too much irrelevant data and the AI will get confused
            
            # Use the raw data to get the CVSS vector 
            messages = [
                CVSS_INSTRUCT_PROMPT,
                CHAIN_OF_THOUGHT_EXAMPLE_DATA_1,
                CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1,
                CHAIN_OF_THOUGHT_EXAMPLE_DATA_2,
                CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2,
                "Data:\n" + input_file_data
            ]

            results = abstract_ai.query(messages)

            vector_strings = self.extract_cvss_vector(results.result_string)

            # Should be only one vector string, but just in case
            vectors = ''
            for cvss_vector_string in vector_strings:
                c = CVSS3(cvss_vector_string)    
                vectors += f"{c.clean_vector()} - Base Score: {c.base_score} - Severity: {c.severities()[0]}\n"
            
            output_text = f"Generated CVSS Vector(s)\n{'-'*80}\n{'-'*80}\n\n{vectors}\nGenerated Evaluation(s)\n{'-'*80}\n{'-'*80}\n\n{results.result_string}\n\nOriginal Data\n{'-'*80}\n{'-'*80}\n\n{input_file_data}"

            print(output_text)

            # Write the output file- if it already exists, overwrite it
            with io.open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(output_text)
            

    def extract_cvss_vector(self, text):
        pattern = r"(CVSS:[0-9.]+\/[A-Za-z0-9:\/]+)+"
        matches = re.findall(pattern, text)
        
        return matches