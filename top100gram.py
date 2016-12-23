#! python 3
#this app scrapes an instagram tracking site for the top 100 accounts

import requests, os, SelenaBot
from bs4 import BeautifulSoup

if os.path.exists('.\\top100pictures') == False:
    os.makedirs('.\\top100pictures') #makes folder to save files in

os.chdir('.\\top100pictures')

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


for account in top100:
	print('accessing '+account+'\'s Instagram')
	SelenaBot.SelenaBot(account)
