import numpy as np
import array
import os

import matplotlib.pyplot as plt

# todo
# put data together to get a big file  1y 3y 5y or all max points for axis
# error checking if file is empty URGENT!!
# todo get time from linecommand and fetch data from files
'''
plt.ylabel('GELD')
x2 = [3, 2.5, 1.0, 1.5, 2.0, 3.5, 4.0, 4.5, 5.0, 6.0]
x = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
plt.plot(x, x2, "r-")
plt.plot(x, x, "k-")
plt.savefig("./bar.png")
plt.show()
'''

for directory in os.listdir(f"./Data"):
    Kurs = []
    Tagestief = []
    Tageshoch = []
    Datum = []
    for stok in sorted(os.listdir(f"./Data/{directory}")):
        data = open(f"./Data/{directory}/{stok}", "r")
        timestart = stok.find("-") + 1
        timeend = stok.find(".")
        Datumdata = int(stok[timestart + 6:timeend])
        name = stok[:timestart - 1]

        Kursdata = data.readlines(1)
        Kursdata = Kursdata[0].replace("Kurs: ", '').replace('\n', '')
        if len(Kursdata) == 0:
            Kursdata = Kurs[-1]
        else:
            Kursdata = float(Kursdata)

        Tagestiefdata = data.readlines(2)
        Tagestiefdata = Tagestiefdata[0].replace(
            'Tagestief: ', '').replace('\n', '')
        if len(Tagestiefdata) == 0:
            Tagestiefdata = Tagestief[-1]
        else:
            Tagestiefdata = float(Tagestiefdata)
            if Tagestiefdata < 1:
                Tagestiefdata = Tagestief[-1]

        Tageshochdata = data.readlines(3)
        Tageshochdata = Tageshochdata[0].replace(
            'Tageshoch: ', '').replace('\n', '')
        if len(Tageshochdata) == 0:
            Tageshochdata = Tageshoch[-1]
        else:
            Tageshochdata = float(Tageshochdata)
            if Tageshochdata < 1:
                Tageshochdata = Tageshoch[-1]

        Datum.append(Datumdata)
        Kurs.append(Kursdata)
        Tagestief.append(Tagestiefdata)
        Tageshoch.append(Tageshochdata)

    print(Datum)
    print(Kurs)
    print(Tagestief)
    print(Tageshoch)

    plt.ylabel('Kurs')
    fig = plt.figure(figsize=(40, 2))
    ax = fig.add_subplot(111)
    plt.plot(Datum, Tagestief, "r-")
    plt.plot(Datum, Kurs, "k-")
    plt.plot(Datum, Tageshoch, "g-")
    plt.savefig(f"./{name}.png")
    # plt.show()
