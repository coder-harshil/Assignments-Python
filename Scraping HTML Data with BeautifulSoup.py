from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import re

lst = []
url = input("Enter link: ")
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

tags = soup('span')

for tag in tags:
    tag = str(tag)
    num = re.findall('[0-9]+', tag)
    for elements in num:
        elements = int(elements)
        lst.append(elements)

print(sum(lst))