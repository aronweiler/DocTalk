import run_local_llm
import run_openai_llm

print("Hello!  Answer some questions to get started.\n")

verbose = input("Should we use verbose output (intermediate steps and such)?  Y/N:").upper()

if input("Run Local LLM: (Y/N)").upper() == "Y":
    top_k = int(input("LOCAL- Select the top_k for search results (how many loaded document results will be used to feed the LLM): "))
    pre_parse_queries = input("LOCAL- Should we pre-parse search queries?  (This could yield different/better results when searching for documents to feed to the LLM)  Y/N:").upper()
    run_local_llm.main(top_k, pre_parse_queries == "Y", verbose == "Y")
else:
    run_openai_llm.main(verbose == "Y")