import io
import os
import argparse
import run_chain

parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--run_open_ai', action='store_true', default=False, help='Use OpenAI vs. local LLM')
parser.add_argument('--database_name', type=str, default="default", help='Database name to use for document storage')
parser.add_argument('--verbose', action='store_true', default=False, help='Verbose mode')
parser.add_argument('--top_k', type=int, default=5, help='Top K value- number of documents or chunks of documents for the LLM to use to answer a question (Note: this can kill performance locally)')
parser.add_argument('--search_distance', type=float, default=0.1, help='Search distance limits the similarity search in the vector database (value should be 0 and 1, lower value indicates a wider search)')
parser.add_argument('--search_type', type=str, default='mmr', help='Search type can be either "similarity", or "mmr". Default is "mmr"')
parser.add_argument('--chain_type', type=str, default='stuff', help='Chain type supported by langchain')
parser.add_argument('--question_file', type=str, required=True, help='Question file')
parser.add_argument('--output_file', type=str, required=True, help='Output file')

# Parse the command-line arguments
args = parser.parse_args()

run_local = args.run_open_ai == False
embedding = run_chain.get_embedding(run_local)
db = run_chain.get_database(embeddings=embedding, database_name=args.database_name)
llm = run_chain.get_llm(run_local)
chain = run_chain.get_chain(llm=llm, memory=None, db=db, top_k=args.top_k, search_type=args.search_type, chain_type=args.chain_type, search_distance=args.search_distance, verbose=args.verbose)

output_text = ''

with io.open(args.question_file, "r") as question_file:
    question_file_data = question_file.read()

questions = question_file_data.split('\n')

for question in questions:
    question = question.strip()
    if len(question) > 0:
        result = chain({"question": question, "chat_history": []})
        
        result_text = result['answer']
        source_docs = "\n".join([f"\t- {os.path.basename(d.metadata['source'])} page {d.metadata['page']}" if 'page' in d.metadata else f"\t- {os.path.basename(d.metadata['source'])}" for d in result["source_documents"]])

        output_text += f"QUESTION: {question}:\n\nANSWER:\n{result_text}\n\nSource Documents:\n{source_docs}\n\n"

with io.open(args.output_file, "w") as file:
    file.write(output_text)

