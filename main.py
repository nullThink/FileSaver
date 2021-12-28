"""
ClassSaver.py

By: Antonio Alphonse (nullThink)
Last Updated: December 28, 2021: 4:42 AM

Purpose: Downloads all of the files from a webpage into the directory of main.py 

TODOS:
    TODO: Make so that this works for any webpage for future classes :)
"""

import requests
import urllib.request
from selenium import webdriver

#initialize Selenium to webpage 
DRIVER_PATH = r'C:\Users\legok\chromedriver_win32\chromedriver'

url = input("What website files are you downloading? ")#"https://www.cs.tufts.edu/comp/15/schedule/schedule.html"

driver = webdriver.Chrome(DRIVER_PATH)

options = webdriver.ChromeOptions();
options.add_argument('headless');

driver.get(url)


# get all of the links on the page and convert from WebDriver objects to 
# the actual redirect links.

objects = driver.find_elements_by_tag_name('a')

links = []

for tag in objects: 
    if(tag.get_attribute("href") != ""):
        links.append(tag.get_attribute("href"))

#get what the filenames would be for each link
filenames = []

for link in links:
    if(link.find('/')):
        try:
            currFilename = link.rsplit('/', 1)[1]
            filenames.append(currFilename)
        except:
            continue;




#downloads each file into the current directory

    #TODO: make download into set directory
    #TODO: Set self organize into folders
filenameCounter = 0;
linkCounter = 0;

while(filenameCounter < len(filenames)):
    
    if(links[linkCounter] != "" and filenames[filenameCounter] != ''):
        r = requests.get(links[linkCounter], allow_redirects=True)
        print(filenames[filenameCounter] + ": " + r.headers.get('content-type'))
    
        if(r.headers.get('content-type') == "html"):
            urllib.request.urlretrieve(links[linkCounter], filenames[filenameCounter])
        elif(r.headers.get('content-type') != "json"):
            with open(filenames[filenameCounter], 'wb') as f:
                f.write(r.content)
    
    filenameCounter = filenameCounter + 1
    linkCounter = linkCounter + 1

