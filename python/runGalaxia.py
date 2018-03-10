#! /usr/bin/env python

from glob import glob
from multiprocessing import Pool
import numpy as np
import os
import random
import sys
from galaxia import Galaxia

#        globallock.release()
def processGalaxia(lon, test=False):
    gal = Galaxia()
    gal.processGalaxia(lon, test=test)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    galaxia = Galaxia()
    Galaxia.pixels = Galaxia.ham.getPixels()
    galaxia.writeHeaders()

    """delete existing lock files"""
    for filename in glob("/var/lock/*"+Galaxia.lockSuffix):
        os.remove(filename)

    """delete old progressFile"""
    if not Galaxia.appendToProgressFile:
        if os.path.isfile(Galaxia.progressFile):
            os.remove(Galaxia.progressFile)

    """delete old Galaxia outputs files"""
#    for filename in glob(os.path.join(Galaxia.dir,"*.ebf*")):
#        os.remove(filename)

    processes = 16
    if processes == 1:
        lon = 175
        processGalaxia(lon, test=True)
    else:
        p = Pool(processes=processes)
        lon = np.arange(Galaxia.lonMin, Galaxia.lonMax+1, 10)
        random.shuffle(lon)
        #    lon = np.arange(5, 360, 10)
        print 'lon = ',lon
        p.map(processGalaxia, lon)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
