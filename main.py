"""
ClassSaver.py

By: Antonio Alphonse (nullThink)
Last Updated: May 15, 2022: 3:33 PM

Purpose: Downloads all of the files from a webpage into the directory of main.py 

Updates:
- Can download youtube videos linked!
- Abstract! Can download from any link!

TODOS:
    DONE: Make so that this works for any webpage for future classes :) 
    TODO: Make so that can work with Canvas. Main Issue: DUO Authentication
    TODO: make download into set directory
    TODO: Set self organize into folders (videos, pdfs, webpages, etc.)
    TODO: Figure out how to do with google docs and online editors
    TODO: Output into a .txt file the links to these pages, with the supplied link at the top

    CHECK: How does it perform on canvas?
    
"""

# Imports
from time import sleep
import requests
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from pytube import YouTube

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))



illegalChar = ["#", "%", "&", "{", "}", "\\", "<", ">", "*", "?", "/", "$", "!", 
"\'", "\"", ":", "@", "+", "`", "|", "="]

#initialize Selenium to webpage 
url = input("What website files are you downloading? ") 

driver.get(url)

# wait for the page to load TODO: make so that it waits on page load instead of arbitrary value
sleep(10)

# get all of the links on the page and convert from WebDriver objects to 
# the actual redirect links.
objects = driver.find_elements(by=By.TAG_NAME, value='a')

rawLinks = []

for tag in objects: 
    if(tag.get_attribute("href") != ""):
        rawLinks.append(tag.get_attribute("href"))

# Remove duplicates in the links in case links are rereferenced
links = []
[links.append(x) for x in rawLinks if x not in links]

# Get links to youtube
ytLinks = []

for link in links:
    try:
        if(("youtube") in link or "youtu.be" in link):
            ytLinks.append(link)
    except:
        continue;


#get what the filenames would be for each link
filenames = []

for link in links:
    try:
        if(link.find('/')):
            currFilename = link.rsplit('/', 1)[1]

            if(filenames.count(currFilename) > 0 and currFilename != "" and links.count(link) == 1):
                minusExtension = currFilename.split(".")
                extension = "." + minusExtension[1]

                currFilename = minusExtension[0] + str(filenames.count(currFilename) + 1) + extension
                
            filenames.append(currFilename)
    except:
        filenames.append("")



#downloads each file into the current directory
filenameCounter = 0;
linkCounter = 0;

notDownloaded = []

# Checks if the current link is a link to a youtube video
def isYT(link):
    isVideo = False

    try:
        isVideo = ytLinks.index(link) >= 0
    except:
        isVideo = False

    return isVideo


# Downloads each file in links
while(filenameCounter < len(filenames)):

    link = links[linkCounter]
    filename = filenames[filenameCounter]

    if(link != "" and filename != '' and not isYT(link)):
        print("Downloading: " + filename)
        # print(link + " " + filename)
        
        r = requests.get(link, allow_redirects=True)
        # print(filename + ": " + r.headers.get('content-type') + "\n")
    
        if(r.headers.get('content-type') == "html"):
            urllib.request.urlretrieve(link, filename)
        elif(r.headers.get('content-type') == "pdf"):
            with open(link, 'wb') as f:
                f.write(r.content)
        elif(r.headers.get('content-type') != "json"):
            try:
                with open(filename, 'wb') as f:
                    f.write(r.content)
            except:
                notDownloaded.append({"link":link, "filename": filename})
    
    filenameCounter = filenameCounter + 1
    linkCounter = linkCounter + 1


# Downloads all youtube videos on supplied page
for video in ytLinks:
    driver.get(video)
    video = driver.current_url.strip()

    try:
        # object creation using YouTube
        # which was imported in the beginning 
        yt = YouTube(video) 

        # filters out all the files with "mp4" extension 
        mp4files = yt.streams.filter(file_extension='mp4', type='video', resolution='720p') 

        title = yt.title.replace(": ", " - ")
        title = title.replace("?","")
        
        print("Downloading: " + title)

        # get the video with the extension and
        # resolution passed in the get() function 

        d_video = yt.streams.get_by_itag(mp4files[0].itag)

        try: 
            # downloading the video
            d_video.download(filename = title + ".mp4") 
        except: 
            notDownloaded.append({"link":video, "filename": "Bad Link"})
            
    except:
        notDownloaded.append({"link":video, "filename": "Connection Error"})
            


# Program Overview
print("\n {0} out of {1} files successfully downloaded. {2} not downloaded.".format(len(links) - len(notDownloaded) - 1 , len(links)-1, len(notDownloaded)))

print(" Not Downloaded:")

for error in notDownloaded:
    print("  -  {0}: {1}".format(error["link"], error["filename"]))
