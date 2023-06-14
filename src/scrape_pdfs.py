import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Obviously my source of documents is a government site haha
#url = "https://www.sandiego.gov/parkandrecboard/meetings"
url = "https://www.sandiego.gov/parkandrecboard/meetings/2022"

#If there is no such folder, the script will create one automatically
folder_location = '/Repos/sample_docs/P&R'
if not os.path.exists(folder_location):os.mkdir(folder_location)

response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")     
for link in soup.select("a[href$='.pdf']"):
    #Name the pdf files using the last portion of each link which are unique in this case
    filename = os.path.join(folder_location,link['href'].split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(requests.get(urljoin(url,link['href'])).content)