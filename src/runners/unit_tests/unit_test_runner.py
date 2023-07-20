import io
from ai.abstract_ai import AbstractAI
from runners.runner import Runner
from runners.unit_tests.configuration.unit_test_runner_configuration import UnitTestRunnerConfiguration
from runners.unit_tests.prompts import CREATE_UNIT_TESTS_PROMPT

class UnitTestRunner(Runner):
    def __init__(self, args):
        super().__init__()
        self.args = UnitTestRunnerConfiguration(args)

    def run(self, abstract_ai: AbstractAI):
        # Create the output file name by taking the code file name and adding '_ut' before the extension
        # For example, if the code file is 'test.py', the output file will be 'test_ut.py'        
        output_file_name = self.args.code_file.split('.')[0] + '_ut.' + self.args.code_file.split('.')[1]

        with io.open(self.args.code_file, "r") as code_file:
            code_file_data = code_file.read()
        
        result = abstract_ai.query(CREATE_UNIT_TESTS_PROMPT.format(language=self.args.language, code=code_file_data))

        with io.open(output_file_name, "w") as output_file:
            output_file.write(result.result_string)