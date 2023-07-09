import io
from ai.abstract_ai import AbstractAI
from runners.runner import Runner

class QuestionFileRunner(Runner):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self, abstract_ai: AbstractAI):
        output_text = ''

        with io.open(self.args["question_file"], "r") as question_file:
            question_file_data = question_file.read()

        questions = question_file_data.split('\n')

        for question in questions:
            question = question.strip()
            if len(question) > 0:
                result = abstract_ai.query(question)
                
                result_text = result.result
                source_docs = "\n".join([f"\t-{doc['document']} - Page {doc['page']}" for doc in result.source_documents])

                output_text += f"QUESTION: {question}:\n\nANSWER:\n{result_text}\n\nSource Documents:\n{source_docs}\n\n"

        with io.open(self.args["answer_file"], "w") as file:
            file.write(output_text)