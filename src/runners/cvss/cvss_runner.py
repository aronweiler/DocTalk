import os
import io
import re
from ai.abstract_ai import AbstractAI
from runners.runner import Runner
from runners.cvss.prompts import  (
    CRITIQUE_PROMPT, 
    CVSS_INSTRUCT_PROMPT, 
    CHAIN_OF_THOUGHT_EXAMPLE_DATA_1, 
    CHAIN_OF_THOUGHT_EXAMPLE_DATA_2, 
    CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1, 
    CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2,
    CRITIQUE_PROMPT_SINGLE_METRIC,
    SINGLE_METRIC_INSTRUCTIONS
)
from runners.cvss.constants import BASE_METRIC_GROUP_ELEMENTS

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
        critique = bool(self.args["critique"])
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

            initial_vectors = self.get_vectors(results.result_string)

            # Are we critiquing?
            critique_printable_results = ''
            if critique:
                critique_printable_results = self._get_critique(abstract_ai, input_file_data, results)
            
            output_text = self._get_final_output(critique_printable_results, initial_vectors, results.result_string, input_file_data)

            print(output_text)

            # Write the output file- if it already exists, overwrite it
            with io.open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(output_text)                        


    def _extract_cvss_vector(self, text):
        pattern = r"(CVSS:[0-9.]+\/[A-Za-z0-9:\/]+)+"
        matches = re.findall(pattern, text)
        
        return matches
    
    def get_vectors(self, result_string):
        vector_strings = self._extract_cvss_vector(result_string)
        
        vectors = ''
        for cvss_vector_string in vector_strings:
            try:
                c = CVSS3(cvss_vector_string)
                vectors += f"{c.clean_vector()} - Base Score: {c.base_score} - Severity: {c.severities()[0]}\n"
            except:
                continue            

        return vectors
    
    def _get_critique(self, abstract_ai, input_file_data, results):

        # Critique the results as one big chunk
        #critique = abstract_ai.query([CRITIQUE_PROMPT.format(instructions=CVSS_INSTRUCT_PROMPT, data=input_file_data, evaluation=results.result_string)])

        single_metric_critique_results =[]
        for metric in SINGLE_METRIC_INSTRUCTIONS:
            # Join the single metric instructions with the single metric critiquing prompt
            single_metric_critique_prompt = CRITIQUE_PROMPT_SINGLE_METRIC.format(instructions=metric[1], metric=metric[0], data=input_file_data, evaluation=results.result_string)

            single_metric_critique_results.append(abstract_ai.query(single_metric_critique_prompt))

        # Join the single metric critiques with the original results
        final_cvss = abstract_ai.query(f"Use the original CVSS evaluation, and the critiqued metrics to create a final CVSS vector.\n\nOriginal Evaluation\n{[results.result_string]}\n\nCritiqued Metrics:\n{[result.result_string for result in single_metric_critique_results]}")

        critique_vectors = self.get_vectors(final_cvss.result_string)

        single_metric_printable_results = "\n\n".join([result.result_string for result in single_metric_critique_results])

        critique_printable_results = f"{'-'*80}\nCritiqued CVSS Vector(s)\n{'-'*80}\n{critique_vectors}\n{'-'*80}\nCritiqued Evaluation(s)\n{'-'*80}\n{single_metric_printable_results}\n\n"

        return critique_printable_results
    
    def _get_final_output(self, critique_printable_results, initial_vectors, result_string, input_file_data):
        output_text = f"""{critique_printable_results}
{'-'*80}
Initial CVSS Vector(s)
{'-'*80}            

{initial_vectors}

{'-'*80}
Initial Evaluation(s)            
{'-'*80}

{result_string}

{'-'*80}
Original Data            
{'-'*80}            

{input_file_data}
            """
        
        return output_text