from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

count = 0
lst = []

#Running an indefinite loop so that program restarts automatically to continue the operation
while True:
    count = count + 1
    if count>7:  #Limit at which program will stop so that users do not have to keep the count
        break
    else: pass
    url = input("Enter link: ")
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup('a')
    for tag in tags:
        lst.append(tag)

    print(lst[17])   #Printing just the desired value
    lst.clear()      #Clearing the list after one loop so that every link's names get added in a fresh list
