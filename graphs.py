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
Kurs = []
Tagestief = []
Tageshoch = []
Datum = []
for directory in os.listdir(f"./Data"):
    for stok in sorted(os.listdir(f"./Data/{directory}")):
        data = open(f"./Data/{directory}/{stok}", "r")
        print(stok)
        timestart = stok.find("-") + 1
        timeend = stok.find(".")
        Datumdata = float(stok[timestart:timeend])

        Kursdata = data.readlines(1)
        Kursdata = float(Kursdata[0].replace("Kurs: ", '').replace('\n', ''))
        print(Kursdata)

        Tagestiefdata = data.readlines(2)
        Tagestiefdata = float(Tagestiefdata[0].replace(
            'Tagestief: ', '').replace('\n', ''))

        Tageshochdata = data.readlines(3)
        Tageshochdata = float(Tageshochdata[0].replace(
            'Tageshoch: ', '').replace('\n', ''))

        Datum.append(Datumdata)
        Kurs.append(Kursdata)
        Tagestief.append(Tagestiefdata)
        Tageshoch.append(Tageshochdata)

    # print(Datum)
    # print(Kurs)
    # print(Tagestief)
    # print(Tageshoch)

    plt.ylabel('Kurs')
    plt.xlabel('Time')

    plt.plot(Datum, Tagestief, "r-")
    plt.plot(Datum, Kurs, "k-")
    plt.plot(Datum, Tageshoch, "g-")
    plt.savefig(f"./{stok}.png")
    # plt.show()
