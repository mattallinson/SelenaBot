# About SelenaBot
SelenaBot is an script that uses BeautifulSoup and JSON to scrape instagram accounts:
* It is named after [Selena Gomez](http://www.instagram.com/selenagomez), the queen of instagram. 
* It only requests the image files for pictures posted the previous day. If you flood instagram/facebook for requests for all image files from an account, they stop responding to all your requests
* It outputs the files in their original JPGs with the filepaths 'username_YYYY-MM-DD_HH-MM'
* Videos are currently downloaded as a JPG of the first frame. I have no need to download video files for my application so this isn't a thing I'm planning on developing.

##the allPics list
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

**Known bug:** Selenabot in its current version garbles the emoji characters into a format that is not only illegible to python, but actually causes it to crash. I've not really got any idea where I'm going wrong with this, and in my current application I'm also not that interested in captions or comments so I've not given it much thought. Since emoji are pretty much universal on *instagram*, I would recommend avoiding trying to read anything under the *captions* or *comments* key

## top100gram
SelenaBot is set up to take images posted by the top 100 most followed instagram accounts. Currently it finds this list by checking [this website](http://socialblade.com/instagram/top/100/followers), although this website doesn't appear to be updated very often. 
