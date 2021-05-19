import json
import urllib.request, urllib.parse, urllib.error

lst = []
url = input("Enter link: ")
html = urllib.request.urlopen(url).read()

data = json.loads(html)
for dicts in data['comments']:              #navigating directly to a dictionary within the dictionary formatted JSON file
    for k,v in dicts.items():
        if k == 'count':
            lst.append(v)

print(sum(lst))

