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
from top100gram import top100

instagram = 'http://www.instagram.com/' 
if os.path.exists('.\\pictures') == False:
    os.makedirs('.\\pictures') 

def DateStamp(ds):
    d = datetime.fromtimestamp(ds)
    return d.strftime('%y-%m-%d_%H-%M-%S')

def SelenaBot(account):
    try:
        rgram = requests.get(instagram + account) #opens specific instagram account
        rgram.raise_for_status()
    except requests.exceptions.HTTPError:
        print('\n\t\t ###ACCOUNT MISSING###\n')
    else:    
        selenaSoup=BeautifulSoup(rgram.text,'html.parser')
        pageJS = selenaSoup.select('script') #selects all the JavaScript on the page
        allPics= json.loads(str(pageJS[6])[52:-10])['entry_data']['ProfilePage'][0]['user']['media']['nodes'] #pulls out information on most recent 12 pictures
        for picture in allPics:
            print('\tDownloading picture '+DateStamp(picture['date']))
            # webbrowser.open(picture['display_src']) #kept here for debugging
            picRes = requests.get(picture['display_src'])
            picFileName = ('.\\pictures\\'+ account+'_'+DateStamp(picture['date'])+'.jpg')
            picFile = open(picFileName,'wb')

            for chunk in picRes.iter_content(100000):
                picFile.write(chunk)

            picFile.close()
                       

for account in top100:
    print('accessing '+account+'\'s Instagram')
    SelenaBot(account)
