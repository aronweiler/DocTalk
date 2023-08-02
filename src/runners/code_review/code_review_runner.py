import logging
import io
from datetime import datetime

from ai.abstract_ai import AbstractAI
from runners.runner import Runner

from runners.code_review.c_plus_plus.c_plus_plus_reviewer import CPlusPlusReviewer

class CodeReviewRunner(Runner):
    def __init__(self, args):
        super().__init__()
        self.args = args
        
        self.supported_languages = {
            "c++": CPlusPlusReviewer,
        }

    def configure(self):
        pass

    def run(self, abstract_ai: AbstractAI):
        language = self.args["language"].lower()

        input_file_name = self.args["code_file"]
        output_file_name = self.args["code_file"] + f"-review-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.md"

        reviewer = self.supported_languages[language](input_file_name)

        output_texts = reviewer.review(abstract_ai)

        if output_texts:
            with io.open(output_file_name, "w") as file:
                file.write('-'*80 + '\n\n'.join(output_texts))
        else:
            logging.warn("No output text to write")