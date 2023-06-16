import os
import time
import utilities.console_text as console_text
from selector import get_llm
import prompts
import documents
from utilities.token_helper import num_tokens_from_string
import utilities.calculate_timing as calculate_timing
import shared
from query_parser import parse_query

def run_chain(initial_query, top_k, llm, db, history, pre_parse_query = False, verbose = False):      
    if pre_parse_query:
        # Get the best keyword query
        document_query = parse_query(query=initial_query)
    else:
        # Just use the initial query
        document_query = initial_query

    print("Document query: ", document_query)

    docs = documents.get_documents(db, document_query, top_k)

    max_estimated_consolidation_time = calculate_timing.calculate_total_processing_time_from_tokens(shared.MAX_LOCAL_CONTEXT_SIZE)
    docs_estimated_processing_time = calculate_timing.calculate_total_processing_time_from_tokens(shared.SPLIT_DOCUMENT_CHUNK_SIZE * len(docs))
    prompt_estimated_processing_time = calculate_timing.calculate_total_processing_time_from_text(prompts.INITIAL_PROMPT_TMPL) * len(docs)
    docs_estimated_processing_time += prompt_estimated_processing_time    

    console_text.print_blue(f"""
    ************
    \nEstimated processing time for retrieving intermediate answers is: {calculate_timing.convert_milliseconds_to_english(docs_estimated_processing_time)}
    \nNote: This does not include the final consolidation query, which will be longer because of the increased context length.
    \nAt most, the final run should take {calculate_timing.convert_milliseconds_to_english(max_estimated_consolidation_time)} (using the largest context size of {shared.MAX_LOCAL_CONTEXT_SIZE})
    \nSo you're probably looking at around {calculate_timing.convert_milliseconds_to_english(max_estimated_consolidation_time + docs_estimated_processing_time)}
    \n************
    """)

    answers = []

    print(f"Creating {len(docs)} initial queries")

    for doc in docs:     
        query = prompts.INITIAL_PROMPT_TMPL.format(question=initial_query, context_str=doc.page_content)        
        
        if verbose:
            print(query)

        print("Query Tokens: ", num_tokens_from_string(query))

        answer = llm(query).strip()

        if len(answer) != 0 and answer != 'No answer given':
            answers.append(answer + f"\nSource: '{os.path.basename(doc.metadata['source'])}'")

        console_text.print_blue(f"\nIntermediate answer: {answer}")      
    
    query = prompts.CONSOLIDATE_ANSWERS_PROMPT_TMPL.format(question=initial_query, answers="\n\t- ".join(answers))        
    
    if verbose:
        print(f"\nFinal Consolidation Query: {query}\n\n")
        print("Consolidation Tokens: ", num_tokens_from_string(query))

    answer = llm(query)

    console_text.print_green(f"\nFinal Answer: {answer}")      

    return answer


def main(top_k, pre_parse_queries, verbose):
    llm = get_llm(True)
    db = documents.get_database(True)

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

        print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time*1000))

