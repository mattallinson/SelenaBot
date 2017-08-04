#! /env/bin/python3

'''
Emoji scraper goes to the unicode website and makes a big long list of the emoji characters maybe
'''

import requests, os, pprint
from bs4 import BeautifulSoup

url = 'http://unicode.org/emoji/charts/full-emoji-list.html'
emoji =[]

r= requests.get(url)
soup = BeautifulSoup(r.text,'html.parser')
emojiSoup = soup.select('.chars')
for e in emojiSoup:
	emoji.append(e.getText())

print(str(emoji))

allEmojiFile = open('emoji.py','w')
allEmojiFile.write('emoji = '+pprint.pformat(emoji)+'\n')  
allEmojiFile.close()