# binpacking.py
#   This file contains a heuristic to translate a given combination of items
#   into a bin packing mapping. Function ed performs the necessary encoding
#   and decoding based on Dahmani (2014).
#   Author: Kristina Spencer
#   Date: March 11, 2016

from __future__ import print_function
import constraints
import numpy as np
import random
from items import makeitems


class BPP:
    # This class groups the bin packing problem information.
    def __init__(self, n, wbin, hbin, items):
        self.n = int(n)         # Number of items to sort
        self.wbin = wbin        # Max. bin weight
        self.ub = hbin          # Max. bin height
        self.items = items      # list of item objects
        self.lb = 0             # initialize lower bound
        self.calclowerbound()

    def calclowerbound(self):
        # This function calculates theoretical lower bound for the number of
        # bins. It assumes this is the total weight of all items divided by
        # the max weight of a bin.
        totalc = 0
        for j in range(self.n):
            totalc += self.items[j].getweight()
        minbin = totalc / self.wbin
        self.lb = int(minbin)

    def getwbin(self):
        # Returns the bin weight limit
        return self.wbin

    def getub(self):
        # Returns the bin height limit
        return self.ub

    def getitems(self):
        # Returns the list of items to pack
        return self.items

    def getlb(self):
        # Returns the theoretical lower bound
        return self.lb


def ed(solid, permutation, bpp):
    # This function follows the algorithm given in Dahmani (2014).
    #  - solid = solution number id
    #  - permutation = list of item indices
    #  - bpp = instance of class BPP
    #   The heuristic used is randomly chosen as indicated in the paper.
    lambba = random.randint(0, 2)
    if lambba == 0:
        x, y = ll(permutation, bpp)
    elif lambba == 1:
        x, y = dp(permutation, bpp)
    else:
        x, y = combo(permutation, bpp)
    # Before returning the x and y matrices, check to make sure the solution
    # is feasible.
    constraints.concheck(solid, x, bpp)
    return x, y


def ll(permutation, bpp):
    # This module decodes a given chromosome "permutation" using
    # the least loaded strategy. It returns x and y, a loading pattern
    # combination. The item index corresponds to the column j + 1.
    m = int(bpp.getlb())    # initialize lower bound on bins
    items = bpp.getitems()
    h, w, n, x, y, r = initial(permutation, bpp)
    for i in range(m):      # initialize y
        y[i] = 1
    for i in range(m):      # initialize r (residual matrix)
        r[i, :] = [w, h]
    # Go through permutation one item at a time.
    for j in range(n):
        item = items[permutation[j] - 1]
        m, x, y, r = llmove(m, w, h, x, y, r, item)
    return x, y


def llmove(m, w, h, x, y, r, item):
    # This module performs the sorting for module ll.
    # Find open bin with max. residual value
    lli = np.argmax(r[0:m, :], axis=0)[1]
    pack = packable(r[lli, 0], r[lli, 1], item)
    # If least loaded bin won't fit item, need to open new bin.
    if pack is False:
        lli = m
    # Get item location in the x matrix
    j = item.getindex() - 1
    m, x, y, r = addtobin(lli, j, m, x, y, r, w, h, item)
    return m, x, y, r


def dp(permutation, bpp):
    # This module decodes a given chromosome "permutation" using
    # the dot product strategy. It returns x and y, a loading pattern
    # combination. The item index corresponds to the column j + 1.
    items = bpp.getitems()
    h, w, n, x, y, r = initial(permutation, bpp)
    m = 1  # open one bin
    y[0] = 1
    r[0, :] = [w, h]
    # Get weights for the dot product array
    weights = scaling(n, items)
    # Go through permutation one item at a time.
    for j in range(n):
        item = items[permutation[j] - 1]
        m, x, y, r = dpmove(m, w, h, x, y, r, item, weights)
    return x, y


def dpmove(m, w, h, x, y, r, item, weights):
    # This module performs the sorting for module dp.
    # Get item location, weight, and height
    j = item.getindex() - 1
    cj = item.getweight()
    hj = item.getheight()
    # Form the dot product array
    dparray = np.zeros(m)
    for i in range(m):
        pack = packable(r[i, 0], r[i, 1], item)
        if pack is True:
            dparray[i] = weights[0] * cj * r[i, 0] + weights[1] * hj * r[i, 1]
    # Find the max. dot product value
    maxdp = np.amax(dparray)
    if maxdp == 0:
        i = m
    else:
        i = np.argmax(dparray)
    m, x, y, r = addtobin(i, j, m, x, y, r, w, h, item)
    return m, x, y, r


def addtobin(i, j, m, x, y, r, w, h, item):
    # If i = m, then a new bin needs to be opened.
    if i == m:
        m += 1
        x[m - 1, j] = 1
        y[m - 1] = 1
        r[m - 1, :] = (w - item.getweight(), h - item.getheight())
    else:
        x[i, j] = 1
        r[i, 0] = r[i, 0] - item.getweight()
        r[i, 1] = r[i, 1] - item.getheight()
    return m, x, y, r


def combo(permutation, bpp):
    # This module decodes the permutation based on the suggested
    # combination of ll and dp strategies in Dahmani (2014).
    split = 0.30
    m = int(bpp.getlb())  # initialize lower bound on bins
    items = bpp.getitems()
    h, w, n, x, y, r = initial(permutation, bpp)
    for i in range(m):  # intialize y
        y[i] = 1
    for i in range(m):  # initialize r (residual matrix)
        r[i, :] = [w, h]
    switch = int(round(n*split))
    # Get weights for the dot product array
    weights = scaling(n, items)
    # Perform least loaded moves before dot product moves.
    for j in range(switch):
        item = items[permutation[j] - 1]
        m, x, y, r = llmove(m, w, h, x, y, r, item)
    for j in range(switch, n):
        item = items[permutation[j] - 1]
        m, x, y, r = dpmove(m, w, h, x, y, r, item, weights)
    return x, y


def initial(permutation, bpp):
    # This module initializes the elements common to all strategies.
    h = int(bpp.getub())  # initialize max length
    w = int(bpp.getwbin())  # initialize max weight
    n = len(permutation)
    x = np.zeros((n, n), dtype=np.int)  # initialize x
    y = np.zeros(n, dtype=np.int)       # initialize y
    r = np.zeros((n, 2), dtype=np.int)  # initialize capacities
    return h, w, n, x, y, r


def scaling(n, items):
    # This module computes the scaling weights for the DP strategy.
    # Weight one is the total weight divided by the # of items.
    # Weight two is the total height divided by the # of items.
    wotot = 0       # Weight one total
    wttot = 0       # Weight two total
    for j in range(n):
        wotot += items[j].getweight()
        wttot += items[j].getheight()
    weights = [wotot / n, wttot / n]
    return weights


def packable(rone, rtwo, item):
    # This module checks to see if object j can fit inside bin i.
    # Weight constraint
    rc = rone - item.getweight()
    # Height constraint
    rh = rtwo - item.getheight()
    # Positive value indicates item will fit
    if rc >= 0:
        if rh >= 0:
            return True
        else:
            return False
    else:
        return False


def repack(x, y, starti, endi, bpp):
    # This module repacks either a bin or multiple bins to comply
    # with constraints.
    # input: x, y, starti (the row of the first bin to repack),
    #        endi (the row after the last bin to repack)
    items = bpp.getitems()
    m, h, w, n, x, y, r, packitems = initialrepack(x, y, starti, endi, bpp)
    lamma = 3 * random.random()
    if lamma < 1:
        # Least loaded strategy
        for j in packitems:
            item = items[j - 1]
            m, x, y, r = llmove(m, w, h, x, y, r, item)
    else:
        # Get weights for the dot product array
        weights = scaling(n, items)
        # Dot product strategy
        if lamma < 2:
            for j in packitems:
                item = items[j - 1]
                m, x, y, r = dpmove(m, w, h, x, y, r, item, weights)
        # Combo strategy
        else:
            split = int(round(0.30 * len(packitems)))
            packitems.sort()
            pack1 = packitems[:split]
            pack2 = packitems[split:]
            for j in pack1:
                item = items[j - 1]
                m, x, y, r = llmove(m, w, h, x, y, r, item)
            for j in pack2:
                item = items[j - 1]
                m, x, y, r = dpmove(m, w, h, x, y, r, item, weights)
    return x, y


def initialrepack(x, y, starti, endi, bpp):
    # This function initializes variables needed for repack
    if y[endi] == 1:        # initialize lower bound on bins
        m = endi
    else:
        m = int(bpp.getlb())
    h = int(bpp.getub())    # initialize max length
    w = int(bpp.getwbin())  # initialize max weight
    n = len(y)              # get number of items
    r = np.zeros((len(y), 2), dtype=np.int)  # initialize capacities
    for i in range(starti, endi):
        r[i, :] = [w, h]
    # Get list of items to repack
    packitems = []
    for i in range(starti, endi):
        if i >= m:
            y[i] = 0
        for j in range(n):
            if x[i, j] == 1:
                packitems.append(j + 1)
                x[i, j] = 0
    return m, h, w, n, x, y, r, packitems


def main():
    # Get info to create items
    # n = eval(input('Please enter the number of items to be sorted: \n'))
    # folder = input('Please enter the name of the folder where your input file is: \n')
    # datafile = input('Please enter the name of the input file: \n')
    n = 500
    folder = '/Users/k9s/Documents/ObjectiveMethod/example/'
    datafile = 'example500.txt'
    random.seed(50)

    # Create item objects and initialize a bin packing problem class
    data = folder + datafile
    binc, binh, items = makeitems(data)
    bpp = BPP(n, binc, binh, items)

    # Input items into the heuristic in the way they were ordered in
    # the datafile. Each "gene" should correspond to an item's index.
    solid = 1                       # give this solution an id number
    chromosome = list(range(1, n + 1))
    x, y = ed(solid, chromosome, bpp)
    np.savetxt(folder + str(solid) + '_x.txt', x, fmt='%i', header='Item Location Matrix x:')
    np.savetxt(folder + str(solid) + '_y.txt', y, fmt='%i', header='Bins Used Matrix y:')


if __name__ == '__main__':
    main()
