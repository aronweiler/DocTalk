import time
import console_text
from llm_selector import get_llm
import prompts
import documents
from token_helper import num_tokens_from_string
from calculate_timing import (calculate_total_processing_time, convert_milliseconds_to_english)


def run_chain(initial_query, top_k, llm, db, history, pre_parse_query = False, verbose = False):      
    if pre_parse_query:
        # Get the best keyword query
        document_query = prompts.PRE_PROCESS_QUERY_PROMPT_TMPL.format(question=initial_query)
        document_query = llm(document_query)
    else:
        # Just use the initial query
        document_query = initial_query

    if verbose:
        print("Document query: ", document_query)

    docs = documents.get_documents(db, document_query, top_k)

    estimated_processing_time = calculate_total_processing_time(docs)

    console_text.print_blue(f"************\nEstimated processing time is: {convert_milliseconds_to_english(estimated_processing_time)}\n************")

    answer = 'No answer yet given'

    answers = []

    for doc in docs:     
        query = prompts.INITIAL_PROMPT_TMPL.format(question=initial_query, context_str=doc.page_content)        
        
        if verbose:
            print(query)

        print("Query Tokens: ", num_tokens_from_string(query))

        answer = llm(query)

        if len(answer.strip()) != 0 and answer.strip() != 'No answer given':
            answers.append(answer)

        console_text.print_blue(f"\nIntermediate answer: {answer}")      
    
    query = prompts.CONSOLIDATE_ANSWERS_PROMPT_TMPL.format(question=initial_query, answers="\n\t- ".join(answers))        
    
    if verbose:
        print(f"\nFinal Consolidation Query: {query}\n\n")
        print("Consolidation Tokens: ", num_tokens_from_string(query))

    answer = llm(query)

    console_text.print_green(f"\nFinal Answer: {answer}")      

    return answer


def main(top_k, pre_parse_queries, verbose = False):
    llm = get_llm()
    db = documents.get_database()

    history = []

    while True:        
        query = input("Query: ")

        if query == "x":
            exit()

        # Time it
        start_time = time.time()
        
        # Run the query
        history.append(run_chain(query, top_k=top_k, llm=llm, db=db, history=history, pre_parse_query=pre_parse_queries, verbose=verbose))
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        print("Operation took: ", convert_milliseconds_to_english(elapsed_time*1000))

main(int(input("top_k: ")), input("pre_parse_queries: (Y/N)").upper() == "Y")