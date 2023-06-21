# DocTalk
DocTalk is a project I'm working on to try to build my own LLM document chat.  

I'm not 100% sure what I'm doing, but it's been great so far.  

*See [Update Notes](#update-notes) for changes I am making after the initial commit to this project.*

Feel free to play around and please for the love of science, give me some feedback.

I legit have no idea if this is going to be useful or anything, but it's certainly teaching me python, and renewing my interest in [snake_case](https://en.wikipedia.org/wiki/Snake_case) variables.

## Usage (python developers)
1. To create the python env, and install requirements, run: [install.ps1](install.ps1)
2. Set your `OPENAI_API_KEY` environment variable, if you are going to use OpenAI's API
3. Load your documents using [document_loader.py](/src/document_loader.py), e.g. `python .\document_loader.py --document_directory="/sample_docs" --database_name="my_db" --run_local`
    - Options for running the document loader include:
      - `--document_directory`: Directory from which to load documents
      - `--database_name`: The name of the database where you'd like to store the loaded documents
      - `--run_open_ai`: When set, this will force the use of the OpenAI LLM and embeddings.  Make sure you set your API key.
      - `--split_documents`: If this is present, the loader will split loaded documents into smaller chunks
      - `--split_chunks`: How big the chunk sizes should be
      - `--split_overlap`: How much of an overlap there should be between chunks
4. Once you've loaded your documents, run the LLM using [run.py](/src/run.py), e.g. `python .\run.py --verbose`
    - Options for running the LLM include:
      - `--run_open_ai`: When set, this will force the use of the OpenAI LLM and embeddings.  Make sure you set your API key.
      - `--database_name`: The name of the database from which to retrieve your documents
      - `--verbose`: When set, outputs more data, such as intermediate steps.
      - `--top_k`: Number of relevant document chunks to pull into the LLM when querying (default is 5)
      - `--search_distance`: Search distance threshold when looking for documents- default is 0.1 (lower # is a broader search)

*Note: the options, such as run_local and database_name, must align between the document loading and the running of the LLM.*

## Usage (non-developers)
*Coming Soon*

## **Random notes** 
The following is mostly copy/paste stuff I use (or used) frequently

### **Creating env**
``` shell
python -m venv doctalk_venv
```

### **Fixing pip issues-- upgrading pip, clearing cache, reinstalling dependencies**
``` shell
python.exe -m pip install --upgrade pip
pip cache purge
pip --no-cache-dir install -r requirements.txt
```
### **Why isn't my llama-cpp working on my GPU?**
Probably because you ran the `/requirements.txt` install before getting here.  Make sure to set these environment variables before installing llama-cpp next time.
``` powershell
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"      
$env:FORCE_CMAKE=1
$env:LLAMA_CUBLAS=1   
```
And this next one is for when you have to force a re-install of llama-cpp because you left the instructions for the GPU below the `/requirements.txt` install 🙄

`pip install --no-cache-dir --force-reinstall llama-cpp-python`

### **Random CUDA Memory Error**
Sometimes a random CUDA memory error will show up.  Use this:
``` powershell
$env:GGML_CUDA_NO_PINNED=1
```

## **TODO List**
- langchain related (although I could do these manually if I want to spend the time learning it??):
  - Add tool to allow LLM to google search and provide answers (google sign in)
  - Add tool to allow the LLM to dynamically retrieve individual documents, vs. pre-processing a folder (e.g. from a website, or local folder)
    - repurpose [scrape_pdfs.py](/scrape_pdfs.py)
- Probably other things
- Documentation??  lol

## **Resources to look at**
- [Question answering using embeddings](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb)
- [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- Best source for models: [TheBloke on HuggingFace](https://huggingface.co/TheBloke)
- [LangChain Dev Blog](https://blog.langchain.dev/)

# Update Notes

- 6/15/2023: 
  - Started to rework the project to separate the local and hosted (OpenAI) LLM stuff.  There are different prompting techniques, and other stuff that I want to play with when it comes to local vs. hosted LLMs.
  - Renamed run_llm.py to run_local_llm.py
  - Added run.py
  - Updated some other random stuff

- 6/20/2023
  - Updated splitting in [document_loader.py](/src/document_loader.py) so that it splits on newlines before hitting the character max.    
  - Added [install.ps1](install.ps1)
  - Added support for top_k in non-local llms

- 6/21/2023
  - Added command line support for [run.py](/src/run.py) and [document_loader.py](/src/document_loader.py)
  - Removed old unused code
  - Collapsed the local and remote LLM access (using langchain) into one file [run_llm_langchain.py](src/run_llm_langchain.py)