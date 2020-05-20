import numpy as np
import os
import matplotlib.pyplot as plt

# todo
# put data together to get a big file  1y 3y 5y or all max points for axis
# think about database mongodb thing stuff
# save in folder to look at with description and stuff
# top line green bottom line red

# todo get time from linecommand and fetch data from files
'''plt.ylabel('GELD')
x2 = [3, 2.5, 1.0, 1.5, 2.0, 3.5, 4.0, 4.5, 5.0, 6.0]
x = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
plt.plot(x, x2, "r-")
plt.plot(x, x, "k-")
plt.savefig("./bar.png")
plt.show()
'''
for stok in os.listdir("./adidas"):
    data = open(f"./adidas/{stok}", "r")
    print(data.read())
