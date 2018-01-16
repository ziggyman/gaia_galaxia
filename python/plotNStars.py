#! /usr/bin/env python

from glob import glob
from multiprocessing import Pool
import os
import shutil
import sys
from numpy import loadtxt

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

import galcomp
import hammer

class Galaxia(object):
    ham = hammer.Hammer()
    pixels = []

    def __init__(self):
        """ do nothing """

    def getOutFileName(self):
        return '/Volumes/yoda/azuri/data/gaia-galaxia/nStarsPerPixel.dat'

    def countStars(self, iPixel):
        print 'iPixel = ',iPixel
        galcomp.countStars(Galaxia.pixels, iPixel, self.getOutFileName())

    def getRedGreenPalette(self):
        colors = []
        for i in range(510):
            b=0
            if i < 255:
                r=255
                g=i
            else:
                g=255
                r=510-i
            colors.append('#%02x%02x%02x' % (r, g, b))

    def plotResult(self):
        lines = loadtxt(self.getOutFileName(), comments="#", delimiter=" ", unpack=False)

        pixelIds = lines[:][0]

        nStarsGalaxia = lines[:][1]
        maxNStarsGalaxia = max(nStarsGalaxia)
        minNStarsGalaxia = max(nStarsGalaxia)

        nStarsGaia = lines[:][2]
        maxNStarsGaia = max(nStarsGaia)
        minNStarsGaia = max(nStarsGaia)

        nStarsFac = nStarsGalaxia / nStarsGaia
        maxNStarsFac = max(nStarsFac)
        minNStarsFac = max(nStarsFac)

        print 'min(nStarsFac) = ',minNStarsFac

        if len(Galaxia.pixels != len(nStarsGaia)):
            print 'ERROR: lengths of pixels(=',len(Galaxia.pixels),') != length of nStarsGaia(=',len(nStarsGaia),')'

        recsGaia = []
        recsGalaxia = []
        recsFac = []
        redGreen = self.getRedGreenPalette()
        for id in pixelIds:
            recsGaia.append(
                Rectangle(
                    (Galaxia.pixels[id].xLow, Galaxia.pixels[id].yLow),   # (x,y)
                     Galaxia.pixels[id].xHigh - Galaxia.pixels[id].xLow,          # width
                     Galaxia.pixels[id].yHigh - Galaxia.pixels[id].yLow,          # height
                     color=redGreen[int((len(redGreen)-1) * nStarsGaia[id] / maxNStarsGaia)]
                )
            )
            recsGalaxia.append(
                Rectangle(
                    (Galaxia.pixels[id].xLow, Galaxia.pixels[id].yLow),   # (x,y)
                     Galaxia.pixels[id].xHigh - Galaxia.pixels[id].xLow,          # width
                     Galaxia.pixels[id].yHigh - Galaxia.pixels[id].yLow,          # height
                     color=redGreen[int((len(redGreen)-1) * nStarsGalaxia[id] / maxNStarsGalaxia)]
                )
            )
            recsFac.append(
                Rectangle(
                    (Galaxia.pixels[id].xLow, Galaxia.pixels[id].yLow),   # (x,y)
                     Galaxia.pixels[id].xHigh - Galaxia.pixels[id].xLow,          # width
                     Galaxia.pixels[id].yHigh - Galaxia.pixels[id].yLow,          # height
                     color=redGreen[int((len(redGreen)-1) * nStarsFac[id] / maxNStarsFac)]
                )
            )
        pcGaia = PatchCollection(recsGaia)
        pcGalaxia = PatchCollection(recsGalaxia)
        pcFac = PatchCollection(recsFac)

        xMin = self.ham.lonLatToXY(-179.999, 0).x
        yMin = self.ham.lonLatToXY(0, -89.999).y

        fig, ax = plt.subplots(1)
        ax.add_collection(pcGaia)
        plt.axis([xMin, -xMin, yMin, -yMin])
        plt.title = 'Gaia'
        plt.show()

        fig, ax = plt.subplots(1)
        ax.add_collection(pcGalaxia)
        plt.axis([xMin, -xMin, yMin, -yMin])
        plt.title = 'Galaxia'
        plt.show()

        fig, ax = plt.subplots(1)
        ax.add_collection(pcFac)
        plt.axis([xMin, -xMin, yMin, -yMin])
        plt.title = 'Fac'
        plt.show()

def processGalaxia(iPix):
    gal = Galaxia()
    gal.countStars(iPix)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """

    gal = Galaxia()
    # remove existing outFile

    # remove existing lock files
    for f in glob('/var/lock/*.lock'):
        os.remove(f)

    if True:
        if os.path.isfile(gal.getOutFileName()):
            shutil.move(gal.getOutFileName(), gal.getOutFileName()+'.bak')

        with open(gal.getOutFileName(), 'w') as f:
            f.write('#PixelId Galaxia Gaia\n')

        ham = hammer.Hammer()
        Galaxia.pixels = ham.getPixels()

        p = Pool(processes=12)
        pix = range(len(Galaxia.pixels))
        p.map(processGalaxia, pix)
        p.close()

    gal.plotResult()

if __name__ == '__main__':
    main(sys.argv)
