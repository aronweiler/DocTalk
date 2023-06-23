#####
## I am using this file to prototype different approaches for searching the stored documents.
## A problem that exists when using Chroma vector database is that it doesn't support keyword search, only similarity searches.
## This means if I am looking for a specific word, e.g. a requirement #, I will often not get that result in the end
##     because the vector db is doing a similarity search on the entire query I've entered.
##
## In the end, I think I will have to have two methods, or even a tool that the LLM uses, to get specific items like this.
#####


from document_loader import get_database
import re

def split_sentence(sentence):
    pattern = r'\b\w+\b'
    words = re.findall(pattern, sentence)
    return words

def search_strings(keywords, strings):
    keyword_count = []
    
    # Count the number of keyword occurrences in each string
    for string in strings:
        count = 0
        for keyword in keywords:
            if keyword.lower() in string.lower():
                count += 1

        if count > 0:                
            keyword_count.append([string, int(count)])
    
    # Sort the strings based on the number of matches
    sorted_strings = sorted(keyword_count, key=lambda x: x[1], reverse=True)
    
    return sorted_strings

def search_stuff():
    db = get_database(True, "work")

    search_terms = split_sentence("What requirements are associated with OSRS11?")
    document_chunks = [d for d in db.get()["documents"]]

    matched_documents = search_strings(["OSRS11", "requirements"], document_chunks)

    results0 = db.similarity_search("OSRS11", filter={"Exact"})
    results1 = db.max_marginal_relevance_search("OSRS11")
    results2 = db.similarity_search("OSRS11")

    #for doc in 


    print(results1[0].page_content)
    print(results2[0].page_content)
    
    
def measure_stuff():
    import utilities.token_helper as token_helper
    
    with open("C:\\Temp\\measure.txt", "r") as f:
        print(token_helper.num_tokens_from_string(f.read()))


measure_stuff()