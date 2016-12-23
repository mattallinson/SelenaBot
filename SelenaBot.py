#! python 3

'''
SelenaBot is an app that uses beautifulsoup
and JSON to scrape instagram accounts.
It is named after Selena Gomez, the queen of instagram.
created by mattallinson
'''

import requests, json, webbrowser, os
from bs4 import BeautifulSoup
from datetime import datetime

instagram = 'http://www.instagram.com/' 

def DateStamp(ds):
    d = datetime.fromtimestamp(ds)
    return d.strftime('%y-%m-%d_%H-%M-%S')

def SelenaBot(account):
    rgram = requests.get(instagram + account) #opens specific instagram account
    selenaSoup=BeautifulSoup(rgram.text,'html.parser')
    pageJS = selenaSoup.select('script') #selects all the JavaScript on the page
    allPics= json.loads(str(pageJS[6])[52:-10])['entry_data']['ProfilePage'][0]['user']['media']['nodes'] #pulls out information on most recent 12 pictures
    for picture in allPics:
        print('\tDownloading picture '+DateStamp(picture['date']))
        # webbrowser.open(picture['display_src']) #kept here for debugging
        picRes = requests.get(picture['display_src'])
        picFileName = (account+'_'+DateStamp(picture['date'])+'.jpg')
        picFile = open(picFileName,'wb')

        for chunk in picRes.iter_content(100000):
            picFile.write(chunk)

        picFile.close()
