import os
from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

import utilities.token_helper as token_helper

from shared import (DOCUMENT_DIRECTORY, DOCUMENT_TYPES, CHROMA_SETTINGS, CHROMA_DIRECTORY, get_embedding)

def load_single_document(file_path: str) -> str:
    # Loads a single document from a file path
    file_extension = os.path.splitext(file_path)[1]
    loader_class = DOCUMENT_TYPES.get(file_extension)
    
    if loader_class:
        loader = loader_class(file_path)
    else:
        raise ValueError("Document type is undefined")
    
    return "\n\n".join([d.page_content for d in loader.load()])# .load_and_split()
    
    
document = load_single_document("/Repos/sample_docs/P&R/prba20220421b.pdf")

print("Tokens in document: ", token_helper.num_tokens_from_string(document))


