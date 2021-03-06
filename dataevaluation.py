import os
import re

# TODO
# Make thing available for index/dax
# make it pretty


def cleanupshares(rawdata):
    # Get Url as string an remove chars to make the search easier
    stoks = str(rawdata.read()).replace(' ', '').replace('/', '')
    # find starting point of information
    start = stoks.find("RightColumn_2") + 16
    end = stoks.find("52WochenHoch")
    # save needed parts
    stok = stoks[start:end]
    # remove all html parts
    counter = 0
    while stok.find("<") != -1:
        if counter == 150:
            print("break")
            break
        counter += 1
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


def cleanupindex(rawdata):
    # Get Url as string an remove chars to make the search easier
    stoks = str(rawdata.read()).replace(' ', '').replace('/', '')

    # find starting point of information
    start = stoks.find("Aktuell")
    end = stoks.find("Jahrestief")
    # saves the needed part
    stok = stoks[start:end]
    # remove all html parts
    counter = 0
    while stok.find("<") != -1:
        if counter == 150:
            print("break")
            break
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

#Print in file


def Writeinfile(stonks, timestamp, Tagestief, Tageshoch, Kurs):
    Data = open(f"./Data/{stonks}/{stonks}-{timestamp}.txt", "w")
    Data.write(
        f"Kurs: {Kurs}\nTagestief: {Tagestief}\nTageshoch: {Tageshoch}\n")
    Data.close()


def Tageswerte(Tag):
    Trennwert = Tag.find(",") + 2
    Tagestiefraw = Tag[Trennwert + 1:]
    Tagestiefraw = Tagestiefraw.replace(',', '.')
    Tageshochraw = Tag[:Trennwert + 1]
    Tageshochraw = Tageshochraw.replace(',', '.')
    return Tageshochraw, Tagestiefraw


if not (os.listdir("./rawdata")):
    os.makedirs("./rawdata")

for folder in os.listdir("./rawdata"):
    if folder != "rawdax":
        for data in os.listdir(f"./rawdata/{folder}"):
            rawdata = open(f"./rawdata/{folder}/{data}", "r")
            name = data.find("-")
            timeend = data.find(".")
            stonks = data[:name]
            timestamp = data[name + 1:timeend]
            if len(timestamp) == 12:
                if not (os.path.isfile(f"./{stonks}/{stonks}-{timestamp}.txt")):
                    stoks = cleanupshares(rawdata)

                    Kurs = courseshares(stoks)
                    Kurs = Kurs.replace(',', '.')
                    Tag = Tageswerteshares(stoks)
                    Tagesresults = Tageswerte(Tag)
                    Tageshoch = Tagesresults[0]
                    Tagestief = Tagesresults[1]
                    if not (os.path.isdir(f"./Data")):
                        os.makedirs(f"./Data")
                    if not(os.path.isdir(f"./Data/{stonks}")):
                        os.makedirs(f"./Data/{stonks}")
                    if not(os.path.isfile(f"./Data/{stonks}/{stonks}-{timestamp}.txt")):
                        Writeinfile(stonks, timestamp,
                                    Tagestief, Tageshoch, Kurs)
    elif folder == "rawdax":
        for data in os.listdir(f"./rawdata/{folder}"):
            rawdata = open(f"./rawdata/{folder}/{data}", "r")
            name = data.find("-")
            timeend = data.find(".")
            stonks = data[:name]
            timestamp = data[name + 1:timeend]
            if len(timestamp) == 12:
                if not (os.path.isfile(f"./{stonks}/{stonks}-{timestamp}.txt")):
                    stoks = cleanupindex(rawdata)

                    Kurs = Kursindex(stoks)
                    Kurs = Kurs.replace(",", ".").replace('.', '', 1)
                    Tag = Tageswerteindex(stoks)
                    Tagesresults = Tageswerte(Tag)
                    Tageshoch = Tagesresults[0]
                    Tagestief = Tagesresults[1]
                    if not (os.path.isdir(f"./Data")):
                        os.makedirs(f"./Data")
                    if not(os.path.isdir(f"./Data/{stonks}")):
                        os.makedirs(f"./Data/{stonks}")
                    if not(os.path.isfile(f"./Data/{stonks}/{stonks}-{timestamp}.txt")):
                        Writeinfile(stonks, timestamp,
                                    Tagestief, Tageshoch, Kurs)
