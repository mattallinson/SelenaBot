#! /.env/bin/python3

'''
BeautifulSoup Instagram Scraper that gets all pictures posted by celebrities yesterday (max 12 pictures per celeb)
'''

import requests
import json
import os
import pprint
import sys
import tweepy
import milpy
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from top100 import top100
from emoji import emoji

#Configuration
instagram = 'http://www.instagram.com/' 
yesterday = (datetime.today()- timedelta(days=1)).strftime('%Y-%m-%d') 
pictureFolder = os.path.join('.','SelenaBot_Pictures',yesterday)
captionFolder = os.path.join('.','SelenaBot_Captions')
emojiFolder = os.path.join('.','SelenaBot_Emoji')
captionFilepath = os.path.join(captionFolder, yesterday +'_captions.txt')
emojiFilepath = os.path.join(emojiFolder, yesterday +'_emoji.txt')

for p in [pictureFolder, captionFolder, emojiFolder]: #makes the prequiste folders, if they don't already exits
    if os.path.exists(p) == False:
        os.makedirs(p) 

def make_twitter_api(profile):
    AUTH_FILE = sys.argv[1]
    with open(AUTH_FILE, "r") as auth_file:
        auth_data = json.load(auth_file)

    profile_auth_data = auth_data[profile]

    auth = tweepy.OAuthHandler(profile_auth_data["consumer_key"],profile_auth_data["consumer_secret"])
    auth.set_access_token(profile_auth_data["access_token"],profile_auth_data["access_secret"])

    return tweepy.API(auth)

def DateStamp(ds):
    d = datetime.fromtimestamp(ds)
    return d.strftime('%y-%m-%d_%H-%M-%S')

def picFinder(account):    
    try:
        rgram = requests.get(instagram + account) #accesses the instagram account
        rgram.raise_for_status()
    except requests.exceptions.HTTPError:	#this handles exceptions if accounts get deleted or suspended. Does not handle exceptions for accounts made private
        print('\t \t ### ACCOUNT MISSING ###')
    else:        
        selenaSoup=BeautifulSoup(rgram.text,'html.parser')
        pageJS = selenaSoup.select('script') #selects all the JavaScript on the page
        for i, j in enumerate(pageJS): #Converts pageJS to list of strings so i can calculate length for below. If BS4 has a neater way of doing this, I haven't found it.
            pageJS[i]=str(j)
        picInfo= sorted(pageJS,key=len, reverse=True)[0] #finds the longest bit of JavaScript on the page, which always contains the image data
        allPics = json.loads(str(picInfo)[52:-10])['entry_data']['ProfilePage'][0]['user']['media']['nodes']

    return allPics

def captionDownloader(picture):
    captions = []
    captionFile = open(captionFilepath,'a')
    if 'caption' in picture.keys():
        print('\tcopying caption for picture '+DateStamp(picture['date']))
        captions.append(picture['caption'])
    captionFile.write(str(captions))
    captionFile.close()

def picDownloader(account):
    for picture in picFinder(account):
        if datetime.fromtimestamp(picture['date']).strftime('%Y-%m-%d') == yesterday: #finds pictures from yesterday
                print('\tDownloading picture '+DateStamp(picture['date']))
                picRes = requests.get(picture['display_src'])
                picFileName = os.path.join(pictureFolder, account+'_'+DateStamp(picture['date'])+'.jpg')
                picFile = open(picFileName,'wb')

                for chunk in picRes.iter_content(100000):
                    picFile.write(chunk)

                picFile.close()
                captionDownloader(picture)

def emojiCounter():
    print('Counting the emojis...')
    captions = open(captionFilepath,'r').read() #opens and read the captions file
    emojiList = []
    for c in captions:
        if c in emoji:
            emojiList.append(c)
    emojiCount= Counter(emojiList)
    topEmoji=emojiCount.most_common(1)
    pprint.pprint(emojiCount) #outputs the count in the terminal
    for i, j in topEmoji:
        print('##########\nthe emoji '+ i +' was used ' +str(j)+' times on instagram yesterday!')
    #saves the count in a text file
    emojiFile= open(emojiFilepath,'w')
    emojiFile.write(pprint.pformat(emojiCount))
    emojiFile.close()


    return topEmoji

    
def main():
    print('downloading pictures:')
    for c, account in enumerate(top100,1):
        print(c,'Pictures from today on '+account+'\'s Instagram')
        picDownloader(account)
    print('finding dominant colour')
    milpy.directory_image_average(pictureFolder, '.jpg')

    if len(sys.argv[1]) > 2:
        api = make_twitter_api('InstaTopEmoji') #updates InstaTopEmoji twitterbot
        for i, j in emojiCounter():
            api.update_status('The most popular emoji on Celebrity Instagram yesterday was: '+ i +' which was used ' +str(j)+' times')

        api = make_twitter_api('instaverage') #updates instaverage twitterbot
        tweetpic = os.path.join(pictureFolder,'1_average_colors.jpg')
        api.update_with_media(tweetpic, status='the dominant colours on Celebrity Instagram yesterday were...')

    else:
        print('no twitter password entered, terminating without tweeting')


if __name__ == '__main__':
    main()