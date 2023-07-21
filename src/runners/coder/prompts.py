SPLIT_INSTRUCTIONS_PROMPT = """Take the following data, representing a description of a software application, and break it down into the sequential steps that would be required to code it in python.
Your output should be a numbered list of steps with each step on a new line.

Your output should look like, "In order to do X, I need to do Y, Z, and A."

Data:
{data}"""

YOU_HAVE_ACCESS_TO = """You have access to the available local components and interfaces:
{local_components}
"""

YOU_HAVE_COMPLETED = """You have already completed the following steps:
{completed_steps}
"""

STEP_INSTRUCTION_PROMPT = """You are coding a software application in Python.

Given the initial description of the application:
{initial_description}

{you_have_completed}

{you_have_access_to}

The step you need to complete is:
{next_step}

Do the following:
    - Identify any libraries that must be imported
    - Create a detailed list of instructions that describe the coding required to complete the step    

Your output should be a list of instructions with each instruction on a new line.
"""

_OLD_STEP_INSTRUCTION_PROMPT = """You are coding a software application in Python.

Given the initial description of the application:
{initial_description}

{you_have_completed}

{you_have_access_to}

The step you need to complete is:
{next_step}

Break the step down into the following sub-steps:
    - Identify any pre-requisite knowledge required to complete the step
    - Identify any components or interfaces that need to be created or modified
    - Identify any data that needs to be created or modified
    - Identify any code that needs to be written or modified
    - Identify any tests that need to be created or modified

Your output should be a numbered list of steps with each step on a new line.
"""

SUB_STEP_INSTRUCTION_PROMPT = """You are coding a software application in Python.

Given the initial description of the application:
{initial_description}

You need to write python code to do the following:

{coding_sub_step}

Modify the following code to include your new code.  If no code needs to be written, return the original code. (ONLY EVER RETURN CODE FROM THIS PROMPT).

{code}
"""