# About SelenaBot
SelenaBot is an script that uses BeautifulSoup and JSON to scrape instagram accounts:
* It is named after [Selena Gomez](http://www.instagram.com/selenagomez), the undisputed queen of instagram. 
* It only requests the image files for pictures posted the previous day. **If you flood instagram/facebook for requests for all image files from an account, they stop responding to all your requests**
* It outputs the files in their original JPGs with the filepaths 'username_YYYY-MM-DD_HH-MM'
* Videos are currently downloaded as a JPG of the first frame. I have no need to download video files for my application so this isn't a thing I'm planning on developing.
* It saves all the comments under all the images scraped in a textfile
* It counts all the emojis used and outputs this as another text file

The main job of SelenaBot is to generate the allPics list. Everything else in SelenaBot.py is dependent on the task you want it to do, based on the imformation in the allPics list. It is currently configured to scrape all the pictures and captions from the day before it is run, and count the frequency of each of the emojis used.



## the allPics list
After crawling the page for the desired account, SelenaBot creates a list called allPics that contains 12 dictionaries, with each dictionary containing the following keys:

* comments_disabled
* video_views
* thumbnail_src
* likes
* code
* date
* id
* caption
* display_src
* is_video
* dimensions
* comments
* owner

These keys are fairly self explanatory. *Date* returns a unix timestamp, *display_src* & *thumbnail_src* return .jpg URLs of large and small versions of the image in question. *Likes* & *Video_Views* return integers of the respective image metrics. Important to note is these dictionary keys don't exist for images where they're irrelevant. E.g. if a picture doesn't have a caption, then the images dictionary wont have the *caption* key. 

## emojiscraper.py
This is a simple BeautifulSoup webscraper which scrapes the [official emoji list](unicode.org/emoji/charts/full-emoji-list.html) to produce emoji.py (see below). I plan to update this so it can automatically check if it's up-to-date.  

## emoji.py 
A python list of all the characters that are emojis. 

### how to use ###
~~~~
$  From emoji import emoji
$ spam = 🍳 
$ spam in emoji
True 
~~~~

'**Skin Tone Modifiers:** Current implementation of selenabot really struggles with Skin Tone Modifiers. It counts them separately to the 'base' emoji that they're modifying. I plan on changing this in the long run, and I expect this process to be [fun](http://dwarffortresswiki.org/index.php/DF2014:Losing).

## top100gram.py
SelenaBot is set up to take images posted by the top 100 most followed instagram accounts. Currently it finds this list by scraping [this website](http://socialblade.com/instagram/top/100/followers) using a BeautifulSoup scraper. This website doesn't appear to be updated very often so I might just replace this with a simple list. 

## Windows
I was originally developing this in windows. However windows hates emojis, making everything crash. Also IDLE hates emojis with similar results. Basically don't use windows or IDLE whenever you need python to do things where you can expect to run into lots of emojis in your strings. 
