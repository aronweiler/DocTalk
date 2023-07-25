import logging
import os
import io
import re
from cvss import CVSS3

from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult
from runners.runner import Runner
from runners.cvss.prompts import  (
    CRITIQUE_PROMPT, 
    CVSS_INSTRUCT_PROMPT, 
    CHAIN_OF_THOUGHT_EXAMPLE_DATA_1,     
    CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1, 
    CHAIN_OF_THOUGHT_EXAMPLE_DATA_2, 
    CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2,    
    CHAIN_OF_THOUGHT_EXAMPLE_DATA_3,
    CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_3,
    CHAIN_OF_THOUGHT_EXAMPLE_DATA_4,
    CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_4,
    CRITIQUE_PROMPT_SINGLE_METRIC,
    SINGLE_METRIC_INSTRUCTIONS,
    SINGLE_METRIC_EVALUATION_PROMPT,
    COMBINE_SINGLE_RESULTS_PROMPT,
    IDENTIFY_VULNERABLE_COMPONENT_PROMPT,
    SINGLE_METRIC_SAMPLE_DATA
)

class CvssRunner(Runner):

    def __init__(self, args):
        super().__init__()
        self.args = args

        self.run_types = {
            "one_shot_evaluation": self.one_shot_evaluation,
            "one_shot_single_critique_evaluation": self.one_shot_single_critique_evaluation,
            "one_shot_iterative_single_metric_critique_evaluation": self.one_shot_iterative_single_metric_critique_evaluation,
            "iterative_single_metric_evaluation": self.iterative_single_metric_evaluation,
            "iterative_single_metric_evaluation_single_critique": self.iterative_single_metric_evaluation_single_critique            
        }

    def run(self, abstract_ai: AbstractAI):

        input_dir = self.args["input_directory"]
        output_dir = self.args["output_directory"]
        run_type = self.args["run_type"]
        all_files = os.listdir(input_dir)        

        for file_path in all_files:
            # Create the input file path
            input_file_path = os.path.join(input_dir, file_path)

            # Skip directories
            if not os.path.isfile(input_file_path):
                continue

            # Create the output file path by appending the run_type as a sub-folder to the output directory, and then appending _analysis to the input file path before the extension
            output_file_path = os.path.join(output_dir, run_type, file_path[:file_path.rfind('.')] + '_analysis' + file_path[file_path.rfind('.'):])
            
            # Read the input file
            with io.open(input_file_path, "r", encoding="utf-8") as input_file:
                input_file_data = input_file.read()

            # Note: we should consider pulling out all of the CVSS relevant data from the input file first- 
            # Sometimes the input file has too much irrelevant data and the AI will get confused

            vulnerable_component = abstract_ai.query(IDENTIFY_VULNERABLE_COMPONENT_PROMPT.format(data=input_file_data)).result_string

            # Call the appropriate run type
            output_text = self.run_types[run_type](abstract_ai, input_file_data, vulnerable_component)            

            logging.debug(output_text)

            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            # Write the output file- if it already exists, overwrite it
            with io.open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(output_text)                        


    def one_shot_evaluation(self, abstract_ai: AbstractAI, input_file_data: str, vulnerable_component: str):        
        messages = self._create_single_shot_input_with_examples(input_file_data, vulnerable_component)

        results = abstract_ai.query(messages)            

        initial_vectors = self._get_vectors(results.result_string)
        
        output_text = self._get_final_output('', initial_vectors, results.result_string, input_file_data)

        return output_text

    def one_shot_single_critique_evaluation(self, abstract_ai: AbstractAI, input_file_data: str, vulnerable_component: str):
        messages = self._create_single_shot_input_with_examples(input_file_data, vulnerable_component)
        results = abstract_ai.query(messages)            

        initial_vectors = self._get_vectors(results.result_string)

        critique_printable_results = self._perform_one_shot_critique(abstract_ai, input_file_data, results.result_string, vulnerable_component)
        
        output_text = self._get_final_output(critique_printable_results, initial_vectors, results.result_string, input_file_data)

        return output_text

    def one_shot_iterative_single_metric_critique_evaluation(self, abstract_ai: AbstractAI, input_file_data: str, vulnerable_component: str):
        messages = self._create_single_shot_input_with_examples(input_file_data, vulnerable_component)
        results = abstract_ai.query(messages)            

        initial_vectors = self._get_vectors(results.result_string)

        critique_printable_results = self._perform_single_metric_critiques(abstract_ai, input_file_data, results)
        
        output_text = self._get_final_output(critique_printable_results, initial_vectors, results.result_string, input_file_data)

        return output_text

    # TODO: Add examples to the input
    def iterative_single_metric_evaluation(self, abstract_ai: AbstractAI, input_file_data: str, vulnerable_component: str):
        # Iterate through the CVSS metrics in SINGLE_METRIC_INSTRUCTIONS and query the AI for each one, using the input_file_data as the input
        results = self._create_iterative_evaluation(abstract_ai, input_file_data, vulnerable_component)
        
        # Next, use the AI to combine all of the results into a single evaluation
        # First, combine the list of results into a single string
        results = '\n'.join(results)
        final_result = abstract_ai.query(COMBINE_SINGLE_RESULTS_PROMPT.format(evaluations=results)).result_string

        initial_vectors = self._get_vectors(final_result)

        output_text = self._get_final_output('', initial_vectors, final_result, input_file_data)

        # Return the final evaluation
        return output_text

    # TODO: Add examples to the input
    def iterative_single_metric_evaluation_single_critique(self, abstract_ai: AbstractAI, input_file_data: str, vulnerable_component: str):
        # Iterate through the CVSS metrics in SINGLE_METRIC_INSTRUCTIONS and query the AI for each one, using the input_file_data as the input
        results = self._create_iterative_evaluation(abstract_ai, input_file_data, vulnerable_component)

        # Next, use the AI to combine all of the results into a single evaluation
        # First, combine the list of results into a single string
        results = '\n'.join(results)
        final_result = abstract_ai.query(COMBINE_SINGLE_RESULTS_PROMPT.format(evaluations=results)).result_string

        critique_printable_results = self._perform_one_shot_critique(abstract_ai, input_file_data, final_result, vulnerable_component)
        
        initial_vectors = self._get_vectors(final_result)
        
        output_text = self._get_final_output(critique_printable_results, initial_vectors, final_result, input_file_data)

        # Return the final evaluation
        return output_text
    
    def _create_iterative_evaluation(self, abstract_ai: AbstractAI, input_file_data: str, vulnerable_component: str):
        results = []
        for metric in SINGLE_METRIC_INSTRUCTIONS:
            # Create the input message
            message = SINGLE_METRIC_EVALUATION_PROMPT.format(metric=metric[0], 
                                                             instructions=metric[1], 
                                                             example_data=SINGLE_METRIC_SAMPLE_DATA, 
                                                             example_evaluation=metric[2], 
                                                             data=input_file_data, 
                                                             vulnerable_component=vulnerable_component)            
            
            # Query the AI
            results.append(abstract_ai.query(message).result_string) 

        return results


    def _create_single_shot_input_with_examples(self, input_file_data: str, vulnerable_component: str):
        messages = [
            CVSS_INSTRUCT_PROMPT.format(vulnerable_component=vulnerable_component),
            CHAIN_OF_THOUGHT_EXAMPLE_DATA_1,
            CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1,
            CHAIN_OF_THOUGHT_EXAMPLE_DATA_2,
            CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2,
            CHAIN_OF_THOUGHT_EXAMPLE_DATA_3,
            CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_3,
            CHAIN_OF_THOUGHT_EXAMPLE_DATA_4,
            CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_4,
            "Data:\n" + input_file_data
        ]

        return messages

    def _extract_cvss_vector(self, text):
        pattern = r"(CVSS:[0-9.]+\/[A-Za-z0-9:\/]+)+"
        matches = re.findall(pattern, text)
        
        return matches
    
    def _get_vectors(self, result_string):
        vector_strings = self._extract_cvss_vector(result_string)
        
        vectors = ''
        for cvss_vector_string in vector_strings:
            try:
                c = CVSS3(cvss_vector_string)
                vectors += f"{c.clean_vector()} - Base Score: {c.base_score} - Severity: {c.severities()[0]}\n"
            except:
                continue            

        return vectors
    
    def _perform_single_metric_critiques(self, abstract_ai: AbstractAI, input_file_data, results: AIResult):
        single_metric_critique_results =[]
        for metric in SINGLE_METRIC_INSTRUCTIONS:
            # Join the single metric instructions with the single metric critiquing prompt
            single_metric_critique_prompt = CRITIQUE_PROMPT_SINGLE_METRIC.format(instructions=metric[1], metric=metric[0], example_data=SINGLE_METRIC_SAMPLE_DATA, example_evaluation=metric[2], data=input_file_data, evaluation=results.result_string)

            single_metric_critique_results.append(abstract_ai.query(single_metric_critique_prompt))

        # Join the single metric critiques with the original results
        final_cvss = abstract_ai.query(f"Use the original CVSS evaluation, and the critiqued metrics to create a final CVSS vector.\n\nOriginal Evaluation\n{results.result_string}\n\nCritiqued Metrics:\n{[result.result_string for result in single_metric_critique_results]}")

        critique_vectors = self._get_vectors(final_cvss.result_string)

        single_metric_printable_results = "\n---\n".join([result.result_string for result in single_metric_critique_results])

        critique_printable_results = f"{'-'*80}\nCritiqued CVSS Vector(s)\n{'-'*80}\n{critique_vectors}\n{'-'*80}\nCritiqued Evaluation(s)\n{'-'*80}\n{single_metric_printable_results}\n\n"

        return critique_printable_results
    
    def _perform_one_shot_critique(self, abstract_ai: AbstractAI, input_file_data, results: str, vulnerable_component: str):

        # Critique the results as one big chunk
        critique = abstract_ai.query([CRITIQUE_PROMPT.format(instructions=CVSS_INSTRUCT_PROMPT.format(vulnerable_component=vulnerable_component), data=input_file_data, evaluation=results)])
        
        critique_vectors = self._get_vectors(critique.result_string)

        critique_printable_results = f"{'-'*80}\nCritiqued CVSS Vector(s)\n{'-'*80}\n{critique_vectors}\n{'-'*80}\nCritiqued Evaluation(s)\n{'-'*80}\n{critique.result_string}\n\n"

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