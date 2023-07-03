import re
import os
import io
from langchain.document_loaders import PDFMinerPDFasHTMLLoader
from bs4 import BeautifulSoup
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

class PDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_page_number(self, html_string):
        pattern = r'<a name="(\d+)">'
        match = re.search(pattern, html_string)
        if match:
            number = int(match.group(1))
            return number
        else:
            return None
    
    def load(self):
        loader = PDFMinerPDFasHTMLLoader(self.file_path)

        data = loader.load()[0]   # entire pdf is loaded as a single Document

        process_doc(data)      

    def process_doc(data:Document):
        soup = BeautifulSoup(data.page_content,'html.parser')
        content = soup.find_all('div')

        cur_page = None
        cur_fs = None
        cur_text = ''
        snippets = []   # first collect all snippets that have the same font size
        for c in content:
            if len(c) > 0:
                temp_page = self.extract_page_number(str(c.contents[0]))  
                if temp_page != None:
                    cur_page = temp_page

            print("Page: ", cur_page)
            sp = c.find('span')
            if not sp:
                continue
            st = sp.get('style')
            if not st:
                continue
            fs = re.findall('font-size:(\d+)px',st)
            if not fs:
                continue
            fs = int(fs[0])
            if not cur_fs:
                cur_fs = fs
            if fs == cur_fs:
                cur_text += c.text
            else:
                snippets.append((cur_text,cur_fs, cur_page))
                cur_fs = fs
                cur_text = c.text
        snippets.append((cur_text,cur_fs, cur_page))
        # Note: The above logic is very straightforward. One can also add more strategies such as removing duplicate snippets (as
        # headers/footers in a PDF appear on multiple pages so if we find duplicatess safe to assume that it is redundant info)


        from langchain.docstore.document import Document
        cur_idx = -1
        semantic_snippets = []
        # Assumption: headings have higher font size than their respective content
        for s in snippets:
            # if current snippet's font size > previous section's heading => it is a new heading
            if not semantic_snippets or s[1] > semantic_snippets[cur_idx].metadata['heading_font']:
                metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1], 'page': s[2]}
                metadata.update(data.metadata)
                semantic_snippets.append(Document(page_content='',metadata=metadata))
                cur_idx += 1
                continue
            
            # if current snippet's font size <= previous section's content => content belongs to the same section (one can also create
            # a tree like structure for sub sections if needed but that may require some more thinking and may be data specific)
            if not semantic_snippets[cur_idx].metadata['content_font'] or s[1] <= semantic_snippets[cur_idx].metadata['content_font']:
                semantic_snippets[cur_idx].page_content += s[0]
                semantic_snippets[cur_idx].metadata['content_font'] = max(s[1], semantic_snippets[cur_idx].metadata['content_font'])
                continue
            
            # if current snippet's font size > previous section's content but less tha previous section's heading than also make a new 
            # section (e.g. title of a pdf will have the highest font size but we don't want it to subsume all sections)
            metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1], 'page': s[2]}
            metadata.update(data.metadata)
            semantic_snippets.append(Document(page_content='',metadata=metadata))
            cur_idx += 1

        return semantic_snippets  
    
file_name = "C:\\Repos\\sample_docs\\Rene\\jul_5\\RWQCB DPEIR Comment_signed.pdf"
fp = open(file_name, 'rb')
parser = PDFParser(fp)    

document = PDFDocument(parser)

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
# from pdfminer.utils import open_filename
#from anyio.streams.memory import create_string_io

# from typing import Container

# page_numbers = []

# output_string = io.StringIO()    
# extract_text_to_fp(
#     fp,  # type: ignore[arg-type]
#     output_string,
#     page_numbers=page_numbers,
#     codec="",
#     laparams=LAParams(),
#     output_type="html",
# )

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter

rsrcmgr = PDFResourceManager()
retstr = io.StringIO()

laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec='', laparams=laparams)
rsrcmgr = PDFResourceManager()
interpreter = PDFPageInterpreter(rsrcmgr, device)

num_pages = 0
page_no = 1
for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
#for page in PDFPage.create_pages(document):    
    num_pages += 1
    interpreter.process_page(page)

    data = retstr.getvalue()

    
    data = ''
    retstr.truncate(0)
    retstr.seek(0)

    page_no += 1

    # output_string = io.StringIO()    
    # extract_text_to_fp(
    #     io.BytesIO(page.contents[0].rawdata),  # type: ignore[arg-type]
    #     output_string,
    #     codec="",
    #     laparams=LAParams(),
    #     output_type="html",
    # )

print(num_pages)


# loader = PDFLoader(file_name)

# docs = loader.load()

#print(docs)