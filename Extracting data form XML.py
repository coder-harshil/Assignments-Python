import xml.etree.ElementTree as ET
import urllib.request, urllib.parse, urllib.error

lst = []
url = input("Enter link: ")

html = urllib.request.urlopen(url).read()

data = ET.fromstring(html)              #program reads and understands XML data
counts = data.findall('.//count')       #finding all 'counts' in the mentioned XML file
for num in counts:
    num = num.text                      #this step ensures that users are able to read their numbers in decoded format
    num = int(num)
    lst.append(num)

print(sum(lst))
