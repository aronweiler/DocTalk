import prompts
import selector

def parse_query(query):
    # always use the local llm to do this
    llm = selector.get_llm(True)

    document_query = prompts.PRE_PROCESS_QUERY_PROMPT_TMPL.format(question=query)
    document_query = llm(document_query)

    return document_query
