import urllib.request
from bs4 import BeautifulSoup
import ssl # Defaults to certificate verification and most secure protocol (now TLS)

# Ignore SSL/TLS certificate error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ').strip()
if len(url) < 1:
    url = 'http://py4e-data.dr-chuck.net/known_by_Fikret.html'

count = int(input("Enter count: ").strip())
pos = int(input("Enter position: ").strip())

for count in range(count+1):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    print(f" Retreiving: {url}")
    
    # Retrieve all anchor tags
    tags = soup('a')
    for i, tag in enumerate(tags, 1):
        if i == pos:
            url = tag.get('href')
            break
    