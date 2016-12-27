#! python 3

'''
SelenaBot is an app that uses beautifulsoup
and JSON to scrape instagram accounts.
It is named after Selena Gomez, the queen of instagram.
created by mattallinson

In this version, it only downloads pictures taken on the day the program is run.
I would like to update it so that it only takes pictures from the past 24 hours

'''

import requests, json, webbrowser, os
from bs4 import BeautifulSoup
from datetime import datetime
from top100gram import top100

def DateStamp(ds):
    d = datetime.fromtimestamp(ds)
    return d.strftime('%y-%m-%d_%H-%M-%S')

instagram = 'http://www.instagram.com/' 
filepath = '.\\' + datetime.now().strftime('%Y-%m-%d')
if os.path.exists(filepath) == False:
    os.makedirs(filepath) 

def SelenaBot(account):
    try:
        rgram = requests.get(instagram + account)
        rgram.raise_for_status()
    except requests.exceptions.HTTPError:
        print('\t \t ### ACCOUNT MISSING ###')
    else:
        rgram = requests.get(instagram + account) #opens specific instagram account
        selenaSoup=BeautifulSoup(rgram.text,'html.parser')
        pageJS = selenaSoup.select('script') #selects all the JavaScript on the page
        allPics= json.loads(str(pageJS[6])[52:-10])['entry_data']['ProfilePage'][0]['user']['media']['nodes'] #pulls out information on most recent 12 pictures
        for picture in allPics:            
            if datetime.fromtimestamp(picture['date']).strftime('%Y/%m/%d') == datetime.now().strftime('%Y/%m/%d'):
                print('\tDownloading picture '+DateStamp(picture['date']))
                #webbrowser.open(picture['display_src']) #kept here for debugging
                picRes = requests.get(picture['display_src'])
                picFileName = (filepath +'\\'+ account+'_'+DateStamp(picture['date'])+'.jpg')
                picFile = open(picFileName,'wb')

                for chunk in picRes.iter_content(100000):
                    picFile.write(chunk)

                picFile.close()
                                       


for account in top100:
    print('Pictures from today on '+account+'\'s Instagram')
    SelenaBot(account)
