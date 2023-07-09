# DocTalk
DocTalk is a project I'm working on to try to build my own LLM document chat.  

I'm not 100% sure what I'm doing, but it's been great so far.  

*See [Update Notes](#update-notes) for changes I am making after the initial commit to this project.*

Feel free to play around and please for the love of science, give me some feedback.

I legit have no idea if this is going to be useful or anything, but it's certainly teaching me python, and renewing my interest in [snake_case](https://en.wikipedia.org/wiki/Snake_case) variables.

## Major Update July 9th, 2023:
I pretty much gutted the project and moved a bunch of things around.  I implemented a different architecture, with the runners and what not. 

Some day soon I will fill the rest of this documentation in!

## Basic Usage (python developers)
1. To create the python env, and install requirements, run: [install.ps1](install.ps1)
2. Set your `OPENAI_API_KEY` environment variable, if you are going to use OpenAI's API. See [.env.template](.env.template) for guidance.
3. Load your documents using [ingest_documents.py](/src/ingest_documents.py)
    - Options for running the document loader include:
      - `--document_directory`: Directory from which to load documents
      - `--database_name`: The name of the database where you'd like to store the loaded documents
      - `--run_open_ai`: When set, this will force the use of the OpenAI LLM and embeddings.  Make sure you set your API key.
      - `--split_documents`: If this is present, the loader will split loaded documents into smaller chunks
      - `--split_chunks`: How big the chunk sizes should be
      - `--split_overlap`: How much of an overlap there should be between chunks
  
4. Select a configuration file [from the configurations folder](configurations/), or create your own
   - Currently there are a few supported AIs and runners- check the [run.py](src/run.py) for the supported types.
5. Once you've loaded your documents, and selected a configuration file, run `run.py --config=<path to config file>`

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
  - Added run_chain.py
  - Updated some other random stuff

- 6/20/2023
  - Updated splitting in [document_loader.py](/src/document_loader.py) so that it splits on newlines before hitting the character max.    
  - Added [install.ps1](install.ps1)
  - Added support for top_k in non-local llms

- 6/21/2023
  - Added command line support for [run_chain.py](/src/run_chain.py) and [document_loader.py](/src/document_loader.py)
  - Removed old unused code
  - Collapsed the local and remote LLM access (using langchain) into one file [run_chain.py](src/run_chain.py)

- 6/23/2023
  - Added multi-document store querying capabilities using [run_react_agent.py](src/run_react_agent.py)
  - Loading user defined tools using [tool_loader.py](src/tool_loader.py)
  - Added an example tool configuration for my work-related stuff, [medical_device_config.json](/tool_configurations/medical_device_config.json)

- 6/24/2023
  - Updated ReAct agent to support self-ask, and call tools in a dynamic way: [run_react_agent.py](src/run_react_agent.py)

- 7/9/2023
  - Major refactor and reorganization
  - Removed a bunch of unused old stuff
  - Implemented selection of AI (QA chain for now) and runners
  - Simplified document ingestion and running
  - Added better support for API
  - Started on getting Docker into the solution