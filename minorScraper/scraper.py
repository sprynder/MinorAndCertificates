import collections
import copy
from ctypes import sizeof
import requests
import json
import unicodedata
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient("mongodb+srv://minor-app-1:minor-app-1@cluster0.ciwey.mongodb.net/?retryWrites=true&w=majority")
db = client['minor-database']
coll = db['minor-collection']

schools = ['architecture','business','communication','education','engineering','fine-arts','geosciences','information','liberal-arts','social-work', 'natural-sciences']

url = ''
linkp1 = 'https://catalog.utexas.edu/undergraduate/'
linkp2 = '/minor-and-certificate-programs/'
finalList = {}

for school in schools:
    url = linkp1 + school + linkp2
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
                                    optionList.append(str(number))
                                    
                    
                    courses[i].append(copy.deepcopy(optionList))    #print(element)
        #print(courses[i])
        finalList[start[i].string] = copy.deepcopy(courses[i])
        # for name in start:
        #     #print(name)
        #     #print(courses[i])
        #     finalList[name.string] = copy.deepcopy(courses[i])


print(finalList)
coll.insert_one(json.loads(json.dumps(finalList)))
#print(start[0].next_element)
#print(start)
#for minor in start:
 #   print(minor)
  #  minor = minor.next_siblings
   # print(minor)
    #while minor not in start:
     #   #if()
      #  minor = minor.next_sibling
client.close()