import praw
import requests
import sys
import os
import json

DEFUALT_PATH = "./"

def downloadFile(url):
    try:
        r = requests.get(url[1], allow_redirects=True)  
        with open(url[0], 'wb') as f:
            f.write(r.content)
        pass
    except:
        print("Download Failed: ")
        pass

def testDestinationExists(destination):
    return os.path.isdir(destination)

def makeDestination():
    if len(sys.argv) == 2:
        if not testDestinationExists(str(sys.argv[1])):
            os.mkdir(str(sys.argv[1]))
            os.chdir(str(sys.argv[1]))
        else:
            os.chdir(str(sys.argv[1]))
    else:
        os.chdir(DEFUALT_PATH)


def bootClient(details):
    reddit = praw.Reddit(client_id = details['client_id'],
                         client_secret = details['client_secret'],
                         user_agent = details['user_agent'])
    return reddit

def bootSubreddit(client,subreddit):
    sub = client.subreddit(subreddit)
    posts = [(s.title, s.url) for s in sub.hot(limit=10000) if ("1080" in s.title
        and "1920" in s.title)]
    return posts

def isPng(url):
    return url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg")


def getPngs(listUrl):
    return [pngs for pngs in listUrl if isPng(pngs[1])]

def replaceSpace(listUrl):
    return [(item[0].replace(" ","_"), item[1]) for item in listUrl]

def initDownload(listUrl):
    [downloadFile(image) for image in listUrl]

def makeFinalName(listUrl):
    return [(item[0] + item[1][-4:], item[1]) for item in listUrl]


def readFile():
    file = open("/home/icemanx7/Python/pythonscripts/subreddits.json", "r", newline=None).read()
    details_json = open("./userdetails.json", "r", newline=None).read()
    json_data = json.loads(file) 
    json_details = json.loads(details_json) 
    subreddits = json_data['subreddits'] 
    print(subreddits)

    for subr in subreddits: 
        print(subr)
        makeDestination()
        r = bootClient(json_details)
        valids = bootSubreddit(r,subr)
        pngList = getPngs(valids)
        finalPngList = replaceSpace(pngList)
        print(len(finalPngList))
        downloadName = makeFinalName(finalPngList)
        print(downloadName)
        initDownload(downloadName)

readFile()
