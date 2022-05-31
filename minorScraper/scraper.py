from ctypes import sizeof
import requests
import json
import unicodedata
from bs4 import BeautifulSoup
url = 'https://catalog.utexas.edu/undergraduate/natural-sciences/minor-and-certificate-programs/'
page = requests.get(url)
text = page.text
soup = BeautifulSoup(page.text, 'html.parser')

#certList = soup.find_all('h3')
list = []
start  = soup.find_all('h3')
minorSize = len(start)
courses = []
dict ={}
for i in range(minorSize):
    courses.append([])

for i in range(minorSize):
    cert = start[i]
    for element in cert.next_siblings:
        #print(type(element))
        if element in start:
            break
        if str(type(element)) == "<class 'bs4.element.Tag'>":
            #print(cert)
            if str(element.name) =='table':
                optionList = []
                for title in element.tbody.children:
                    if str(type(title)) == "<class 'bs4.element.Tag'>" and 'class' in title.attrs:
                        #print(title.td['class'])
                        #If attras hs class and its 2, then its a hours coloumn
                        if 'class' in title.td.attrs.keys() and 'colspan' not in title.td.attrs.keys():
                            #print(str(title.td['class']))
                            if(str(title.td['class'])=="['codecol']" or str(title.td['class'])=="['orclass']"):
                                #print(title.td)
                                number = title.td.a['title']
                                number = unicodedata.normalize("NFKD",number)
                                cname = title.find_all('td')[1].string
                                dict[number] = cname
                                optionList.append(number)
                                #print(number, " ", cname)
                courses[i].append(optionList)    #print(element)
            
#print(dict)
#print(courses)
finalList = {}
for name in start:
    finalList[name.string] = courses[i]
print(finalList)
#print(start[0].next_element)
#print(start)
#for minor in start:
 #   print(minor)
  #  minor = minor.next_siblings
   # print(minor)
    #while minor not in start:
     #   #if()
      #  minor = minor.next_sibling
    