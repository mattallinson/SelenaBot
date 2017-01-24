#! /env/bin/python3

'''
BeautifulSoup Instagram Scraper that gets all pictures posted by celebrities yeterday (max 12 pictures per celeb)
'''

import requests, json, os, collections, pprint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from top100gram import top100
from emoji import emoji

instagram = 'http://www.instagram.com/' 
yesterday = (datetime.today()- timedelta(days=1)).strftime('%Y-%m-%d') 
pictureFilepath = os.path.join('.','SelenaBot_Pictures',yesterday)
captionFilepath = os.path.join('.','SelenaBot_Captions')
emojiFilepath = os.path.join('.','SelenaBot_Emoji')
captions = []

for p in [pictureFilepath, captionFilepath, emojiFilepath]:
    if os.path.exists(p) == False:
        os.makedirs(p) 

def DateStamp(ds):
    d = datetime.fromtimestamp(ds)
    return d.strftime('%y-%m-%d_%H-%M-%S')

def SelenaBot(account):
    try:
        rgram = requests.get(instagram + account)
        rgram.raise_for_status()
    except requests.exceptions.HTTPError:	#this handles exceptions if accounts get deleted or suspended. Does not handle exceptions for accounts made private
        print('\t \t ### ACCOUNT MISSING ###')
    else:
        #rgram = requests.get(instagram + account) #opens specific instagram account
        selenaSoup=BeautifulSoup(rgram.text,'html.parser')
        pageJS = selenaSoup.select('script') #selects all the JavaScript on the page
        allPics= json.loads(str(pageJS[6])[52:-10])['entry_data']['ProfilePage'][0]['user']['media']['nodes'] # pulls out information on most recent 12 pictures into a list called "All Pics"
        for picture in allPics:            
            if datetime.fromtimestamp(picture['date']).strftime('%Y-%m-%d') == yesterday: #finds pictures from yesterday
                print('\tDownloading picture '+DateStamp(picture['date']))
                picRes = requests.get(picture['display_src'])
                picFileName = os.path.join(pictureFilepath, account+'_'+DateStamp(picture['date'])+'.jpg')
                picFile = open(picFileName,'wb')

                for chunk in picRes.iter_content(100000):
                    picFile.write(chunk)

                picFile.close()
                #if the picture has a caption, adds it to the "captions" list
                if 'caption' in picture.keys():
                    print('\tcopying caption for picture '+DateStamp(picture['date']))
                    captions.append(picture['caption'])
    
    #saves the captions list to a text file. 
    captionFile = open(os.path.join(captionFilepath, yesterday +'_captions.txt'),'w')
    captionFile.write(str(captions))
    captionFile.close() 

for account in top100:
    print('Pictures from today on '+account+'\'s Instagram')
    SelenaBot(account)


#Pulls out the emojis from all the captions and counts them
captionsString =''.join(captions)
char = []
for c in captionsString:
    if c in emoji:
        char.append(c)
        
pprint.pprint(collections.Counter(char)) #outputs the count in the terminal
#saves the count in a text file
emojiFile= open(os.path.join(emojiFilepath, yesterday +'_emoji.txt'),'w')
emojiFile.write(pprint.pformat(collections.Counter(char)))
emojiFile.close()
