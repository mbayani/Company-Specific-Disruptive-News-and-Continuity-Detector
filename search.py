from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
  
# to search 
query = input("Enter the company's name : ")
   

url=[]
for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
    url.append(j)

company_info=[]


for i in range(0,len(url)):
    req = Request(url[i], headers={'User-Agent': 'Mozilla/5.0'})
    html=urlopen(req).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    li=list(text.split(" "))
    company_info.append(li)    

print(company_info)
