import argparse
import json

from ai.qa_chain import QAChainAI
from api.rest_api_runner import RestAPIRunner
from console.console_runner import ConsoleRunner

RUN_TYPES = {
    "qa_chain": QAChainAI,
    # TODO: this
    # "agent_with_tools" : xxx
}

RUN_MODES = {
    "api": RestAPIRunner,
    "console" : ConsoleRunner,
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

ai_type = config['ai_type']
run_mode = config['run_mode']
config_args = config['arguments']

# start the application in the specified mode for the specified type

# get the ai
ai_class = RUN_TYPES.get(ai_type)
if ai_class:
    ai = ai_class()
    ai.configure(config_args['arguments'])
else:
    raise ValueError(f"ai_type is undefined, {ai_type}")

# run the mode
runner_class = RUN_MODES.get(run_mode)
if runner_class:
    runner = runner_class()
    if callable(runner):
        runner(ai) # This is here because starting FastAPI in proc demands it (see the RestAPIRunner)
    runner.run(abstract_ai=ai)
else:
    raise ValueError(f"mode is undefined, {run_mode}")


# testing
# result = ai.query("Summarize what the documents say about: Sea level rise ")
# print(result)
