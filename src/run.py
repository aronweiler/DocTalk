import run_local_llm

print("Hello!  Answer some questions to get started.\n")

top_k = int(input("Select the top_k for search results (how many loaded document results will be used to feed the LLM): "))
pre_parse_queries = input("Should we pre-parse search queries?  (This could yield different/better results when searching for documents to feed to the LLM)  Y/N:").upper()
verbose = input("Should we output intermediate steps?  Y/N:").upper()

if input("Run Local LLM: (Y/N)").upper() == "Y":
    run_local_llm.main(top_k, pre_parse_queries == "Y", verbose == "Y")
else:
    print("Not ready yet....")