#! python 3
'''
this app scrapes an instagram tracking site for the top 100 accounts
'''

import requests, os
from bs4 import BeautifulSoup

r = requests.get('https://socialblade.com/instagram/top/100/followers') #access instagram tracking site
soup = BeautifulSoup(r.text, "html.parser")
grams = soup.find_all('div', class_="table-cell") #scrapes the content from the table on the page

top100 = []                             #produces top100 list
for g in grams:                          # populates top 100 list
    a = g.find("a")
    if a is not None:
        top100.append(a.get_text())

if 'justinbieber' in top100:    #Cleans up "Justin Bieber bug" 
    top100.remove('justinbieber') 
    top100.append('justnbieber')

t100file = open('top100.txt','w')
t100file.write(str(top100))  
t100file.close()
