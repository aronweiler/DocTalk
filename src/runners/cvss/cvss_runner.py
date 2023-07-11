import os
import io
import re
from ai.abstract_ai import AbstractAI
from runners.runner import Runner
from runners.cvss.prompts import BASE_METRIC_PROMPT, METRICS_TABLE, CVSS_INSTRUCT_PROMPT, CRITIQUE_PROMPT, DETAILED_BASE_METRICS_INSTRUCTIONS

from utilities.token_helper import num_tokens_from_string

from cvss import CVSS3

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

            # First, attempt to pull out all of the CVSS relevant data from the input file
            # prompt = f"Extract data points (in a list format) from the following data that could be used to generate a CVSS vector string.  Be sure to include an explanation as to why you selected each data point.\n\nData:\n{input_file_data}"
            # extracted_data_points = abstract_ai.query(prompt).result
            # print("Extracted data points: ", extracted_data_points)
            
            # # Use the extracted data to get the CVSS vector 
            # prompt = CVSS_INSTRUCT_PROMPT.format(data=extracted_data_points)
            # extracted_data_result = abstract_ai.query(prompt)
            # print("Extracted data points evaluation result: ", extracted_data_result.result)

            # Use the raw data to get the CVSS vector 
            prompt = CVSS_INSTRUCT_PROMPT.format(data=input_file_data)
            print("Number of tokens in prompt: ", num_tokens_from_string(prompt))
            raw_data_result = abstract_ai.query(prompt)
            print("Raw data evaluation result: ", raw_data_result.result)

            # Have the AI use the raw data evaluation and the original file data to critique the reasoning behind the CVSS vector, and improve the evaluation if possible.
            # prompt = CRITIQUE_PROMPT.format(instructions=DETAILED_BASE_METRICS_INSTRUCTIONS, data=input_file_data, evaluation=raw_data_result.result)
            # print("Number of tokens in prompt: ", num_tokens_from_string(prompt))
            # critique_result = abstract_ai.query(prompt)
            # print("Critique result: ", critique_result.result)

            # Have the AI pull from both the extracted data and the raw data to get the best representation of the data
            # prompt = f"Combine the following two results into a single response, removing any duplication, but keeping the CVSS vector and all of the reasoning intact:\n\nExtracted Data:\n{extracted_data_result.result}\n\nRaw Data:\n{raw_data_result.result}"
            # result = abstract_ai.query(prompt)

            raw_data_vector_strings = self.extract_cvss_vector(raw_data_result.result)
            #critique_vector_strings = self.extract_cvss_vector(critique_result.result)

            vectors = ''
            for cvss_vector_string in raw_data_vector_strings:
                c = CVSS3(cvss_vector_string)    
                vectors += f"\nInitial Evaluation: {c.clean_vector()}\nBase Score: {c.base_score} ({c.severities()[0]})"
            
            # for cvss_vector_string in critique_vector_strings:
            #     c = CVSS3(cvss_vector_string)    
            #     vectors += f"\nCritique Evaluation: {c.clean_vector()}\nBase Score: {c.base_score} ({c.severities()[0]})"
            
            # Output with critique
            #output_text = f"Initial Evaluation:\n{raw_data_result.result}\n\nCritique Evaluation:\n{critique_result.result}\n{vectors}\n\nInput File: {input_file_path}"

            # Output without critique
            output_text = f"Initial Evaluation:\n{raw_data_result.result}\n{vectors}\n\nInput File: {input_file_path}"

            with io.open(output_file_path, "w") as file:
                file.write(output_text)    

    def extract_cvss_vector(self, text):
        pattern = r"(CVSS:[0-9.]+\/[A-Za-z0-9:\/]+)+"
        matches = re.findall(pattern, text)
        
        return matches