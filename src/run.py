import argparse
import json

from ai.qa_chain import QAChainAI
from ai.llm_chain import LLMChain
from ai.react_agent import ReActAgent
from runners.api.rest_api_runner import RestAPIRunner
from runners.console.console_runner import ConsoleRunner
from runners.question_file.question_file_runner import QuestionFileRunner
from runners.cvss.cvss_runner import CvssRunner

AI_TYPES = {
    "qa_chain": QAChainAI,
    "agent_with_tools" : ReActAgent,
    "llm_chain": LLMChain
}

RUNNER_TYPES = {
    "api": RestAPIRunner,
    "console" : ConsoleRunner,
    "question_file": QuestionFileRunner,
    "cvss": CvssRunner
    # TODO: this     
    # "web_ui" : xxx,
}

parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--config', type=str, required=True, help='Path to the configuration file')

# Parse the command-line arguments
args = parser.parse_args()

# load the config
with open(args.config) as config_file:
    config = json.load(config_file)

ai_type = config['ai']['type']
ai_args = config['ai']['arguments']

runner_type = config['runner']['type']
runner_args = config['runner']['arguments']

print("ai_type: ", ai_type)

# Print out the list of arguments in a nice human readable format: 
print("ai_args:")
for key, value in ai_args.items():
    print(f"\t{key}: {value}")

print("runner_type: ", runner_type)

# Print out the list of arguments in a nice human readable format:
print("runner_args:")
for key, value in runner_args.items():
    print(f"\t{key}: {value}")

# start the application in the specified mode for the specified type

# get the ai
ai_class = AI_TYPES.get(ai_type)
if ai_class:
    ai = ai_class()
    ai.configure(ai_args)
else:
    raise ValueError(f"ai_type is undefined, {ai_type}")

# run the mode
runner_class = RUNNER_TYPES.get(runner_type)
if runner_class:    
    # If there are arguments in the runner config, pass them on
    if runner_args:
        runner = runner_class(runner_args)
    else:
        runner = runner_class()

    if callable(runner):
        runner(ai) # This is here because starting FastAPI in proc demands it (see the RestAPIRunner)
    runner.run(abstract_ai=ai)
else:
    raise ValueError(f"mode is undefined, {runner_type}")


# testing
# result = ai.query("Summarize what the documents say about: Sea level rise ")
# print(result)
