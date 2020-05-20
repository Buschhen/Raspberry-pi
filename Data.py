import requests
import re
import sys
import os.path
import time
from datetime import datetime
from os import path

# TODO
# good var names
# error checking


'''
For the index 
'''
# Get the time stamp for filename and to check time


def unixtimer():
    # format to string
    timestamp = str(datetime.now())
    timestamp = timestamp.replace(' ', '').replace(':', '').replace('-', '')
    dot = timestamp.find(".") - 2
    # format time to cut of seconds
    unix = timestamp[0:dot]
    unix = int(unix)
    return unix

# Clean up the information to read important data


def cleanupindex(url):
    # Get Url as string an remove chars to make the search easier
    site = str(requests.get(url).content).replace(
        '\\t', '').replace('\\n', "").replace('\\r', '').replace(' ', '').replace('/', '')
    # find starting point of information
    start = site.find("Aktuell")
    end = site.find("Jahrestief")
    # saves the needed part
    stok = site[start:end]
    # remove all html parts
    while stok.find("<") != -1:
        start = stok.find("<")
        end = stok.find(">")
        stok = stok[0:start:] + stok[end + 1::]
    return stok

# Get the Current course


def Kursindex(stoks):
    Kurs_start = stoks.find("Kurs") + 4
    Kurs_ende = stoks.find(",", Kurs_start) + 3
    Kurswerte = stoks[Kurs_start:Kurs_ende]
    return Kurswerte

# Get array with day min and day max


def Tageswerteindex(stoks):
    # get the point from where the number starts
    Tagestief_start = stoks.find("Tageshoch") + 9
    Tagestief_end = Tagestief_start
    while re.search("[,-9]", stoks[Tagestief_end]):
        Tagestief_end += 1
        if Tagestief_end == len(stoks):
            break
    minmaxwerte = stoks[Tagestief_start:Tagestief_end]
    return minmaxwerte


'''
For the shares
'''


def cleanupshares(url):
    # Get Url as string an remove chars to make the search easier
    site = str(requests.get(url).content).replace(
        '\\t', '').replace('\\n', "").replace('\\r', '').replace(' ', '').replace('/', '')
    # find starting point of information
    start = site.find("RightColumn_2") + 16
    end = site.find("52WochenHoch")
    # save needed parts
    stok = site[start:end]
    # remove all html parts
    while stok.find("<") != -1:
        start = stok.find("<")
        end = stok.find(">")
        stok = stok[0:start:] + stok[end + 1::]
    return stok


# Get the Current course
def courseshares(stoks):
    Kurs_start = stoks.find("Kurs") + 4
    Kurs_ende = Kurs_start
    while re.search("[,-9]", stoks[Kurs_ende]):
        Kurs_ende += 1
    Kurswerte = stoks[Kurs_start:Kurs_ende]
    return Kurswerte

# Get array with day min and day max


def Tageswerteshares(stoks):
    # get the point from where the number starts
    Tagestief_start = stoks.find("Tagestief") + 9
    Tagestief_end = Tagestief_start
    while re.search("[,-9]", stoks[Tagestief_end]):
        Tagestief_end += 1
        if Tagestief_end == len(stoks):
            break
    minmaxwerte = stoks[Tagestief_start:Tagestief_end]
    return minmaxwerte


#Print in file


def Writeinfile(stonks, unixtime, Tagestief, Tageshoch, Kurs):
    Data = open(f"./{stonks}/{stonks}-{unixtime}.txt", "a")
    Data.write(
        f"Kurs: {Kurs}\nTagestief: {Tagestief}\nTageshoch: {Tageshoch}\n")
    Data.close()


def main():
    while True:
        unixtime = unixtimer()
        if unixtime % 10 == 0:
            urls = open("URLS.txt", "r")
            for line in urls:
                url = line.strip()
                if url.find("index") > 0:

                    stonks = url[url.find("index") + 6:]
                    # check if file exitst if true skip

                    if not (os.path.isfile(f"./{stonks}/{stonks}-{unixtime}.txt")):

                        stoks = cleanupindex(url)

                        Kurs = Kursindex(stoks)

                        Tag = Tageswerteindex(stoks)
                        # the values have 2 decimal poinsts and are stuk together so you need to split one number in to
                        Trennwert = Tag.find(",") + 2
                        Tagestief = Tag[0: Trennwert+1]
                        Tageshoch = Tag[Trennwert + 1:]

                        if not(os.path.isdir(f"./{stonks}")):
                            os.makedirs(f"{stonks}")
                        Writeinfile(stonks, unixtime,
                                    Tagestief, Tageshoch, Kurs)

                elif url.find("aktien") > 0:
                    stonks = url[url.find("aktien") + 7:url.find("-")]
                    if not (os.path.isfile(f"./{stonks}/{stonks}-{unixtime}.txt")):

                        stoks = cleanupshares(url)

                        Kurs = courseshares(stoks)

                        Tag = Tageswerteshares(stoks)

                        # the values have 2 decimal poinsts and are stuk together so you need to split one number in to
                        Trennwert = Tag.find(",") + 2
                        Tagestief = Tag[0: Trennwert+1]
                        Tageshoch = Tag[Trennwert + 1:]

                        if not(os.path.isdir(f"./{stonks}")):
                            os.makedirs(f"{stonks}")
                        Writeinfile(stonks, unixtime,
                                    Tagestief, Tageshoch, Kurs)
                else:
                    print("Sorry cant look up this site")


if __name__ == '__main__':
    main()
