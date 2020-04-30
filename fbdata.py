import os
import sys
import datetime
import facebook
import csv
import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve 


def coldata():
    gettoday = datetime.datetime.now()
    token = 'EAACEdEose0cBAPZCCCTJGe1vQINixQCEPnXsZAJIu5taLnAoQ52oReJyjjdqz1LZBwqXCg2GCFikkDOtuSZCJZBgpUGpZAuDStIUT03uIPdTCxog3xZBG7wOR3uwlukfcmhtwp18RRj9uhtGZAztDeB8u1eNUWIwtyaaa56E6agw6kOeeUezMcfmYzH14qTEld8ZD'
    # findid = '64637653943'
    from getcsvdata import readcsvintocode
    from getcsvdata import getfbdata
    getall = readcsvintocode.readcsv("D:\\python\\NBAplayer.csv")
    getall2 = readcsvintocode.readcsv2("D:\\python\\Artist ID.csv")
    getall3 = readcsvintocode.readcsv2("D:\\python\\MLB-fb.csv")
    # print(len(getall))

    for index in range(len(getall)):
        try:
            getfbdata.writealldata(token, getall[index][2], getall[index][0], getall[index][1])
        except:
            print("no data "+getall[index][1])
    
    for index in range(len(getall2)):
        try:
            getfbdata.writealldata2(token, getall2[index][2], getall2[index][0], getall2[index][1])
        except:
            print("no data "+getall2[index][1])
        # getfbdata.writealldata2(token, getall2[index][2], getall2[index][0], getall2[index][1])

    for index in range(len(getall3)):
        try:
            getfbdata.writealldata2(token, getall3[index][0], getall3[index][2], getall3[index][1])
        except:
            print("no data "+getall3[index][1])

coldata()