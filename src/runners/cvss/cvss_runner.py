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
                SystemMessage(content=CVSS_INSTRUCT_PROMPT),
                HumanMessage(content=CHAIN_OF_THOUGHT_EXAMPLE_DATA_1, example=True),
                AIMessage(content=CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1, example=True),
                HumanMessage(content=CHAIN_OF_THOUGHT_EXAMPLE_DATA_2, example=True),
                AIMessage(content=CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2, example=True),
                HumanMessage(content="DATA:\n" + input_file_data)
            ]

            raw_data_result = abstract_ai.query(messages)
            print("Evaluation result: ", raw_data_result.result_string)

            raw_data_vector_strings = self.extract_cvss_vector(raw_data_result.result_string)

            vectors = ''
            for cvss_vector_string in raw_data_vector_strings:
                c = CVSS3(cvss_vector_string)    
                vectors += f"\nInitial Evaluation: {c.clean_vector()}\nBase Score: {c.base_score} ({c.severities()[0]})"
            
            output_text = f"Initial Evaluation:\n{raw_data_result.result_string}\n{vectors}\n\nInput File: {input_file_path}"

            with io.open(output_file_path, "w") as file:
                file.write(output_text)    

    def extract_cvss_vector(self, text):
        pattern = r"(CVSS:[0-9.]+\/[A-Za-z0-9:\/]+)+"
        matches = re.findall(pattern, text)
        
        return matches