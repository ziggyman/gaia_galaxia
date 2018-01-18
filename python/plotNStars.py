#! /usr/bin/env python

from glob import glob
from multiprocessing import Pool
import os
import shutil
import sys
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

import galcomp
import hammer

class Galaxia(object):
    ham = hammer.Hammer()
    pixels = []
    whichOne = 'gaiaTgas'

    def __init__(self):
        """ do nothing """

    def getOutFileName(self):
        if Galaxia.whichOne == "gaiaTgas":
            return '/Volumes/yoda/azuri/data/gaiaTgas-galaxia/nStarsPerPixel.dat'
        elif Galaxia.whichOne == "gaia":
            return '/Volumes/yoda/azuri/data/gaia-galaxia/nStarsPerPixel.dat'
        else:
            print 'Galaxia.getOutFileName: ERROR: Galaxia.whichOne(=',Galaxia.whichOne,') not found in [gaia, gaiaTgas]'
            STOP

    def countStars(self, iPixel):
        print 'iPixel = ',iPixel
        galcomp.countStars(Galaxia.pixels, iPixel, self.getOutFileName(), Galaxia.whichOne)

    def getRedGreenPalette(self):
        colors = []
        for i in np.arange(0.0,510.0):
            b=0.0
            if i < 255.0:
                r=1.0
                g=i/255.0
            else:
                g=1.0
                r=(510.0-i)/255.0
            colors.append((r, g, b))
        return colors

    def plotResult(self):
        lines = np.loadtxt(self.getOutFileName(), comments="#", delimiter=" ", unpack=False)

        pixelIds = lines[:,0].astype(int)

        nStarsGalaxia = lines[:,1].astype(float)
        maxNStarsGalaxia = max(nStarsGalaxia)
        minNStarsGalaxia = min(nStarsGalaxia)

        nStarsGaia = lines[:,2].astype(float)
        maxNStarsGaia = max(nStarsGaia)
        minNStarsGaia = min(nStarsGaia)

        nStarsFac = nStarsGalaxia / nStarsGaia
        maxNStarsFac = max(nStarsFac)
        minNStarsFac = min(nStarsFac)

        print 'min(nStarsGaia) = ',minNStarsGaia, ', max(nStarsGaia) = ',maxNStarsGaia
        print 'min(nStarsGalaxia) = ',minNStarsGalaxia, ', max(nStarsGalaxia) = ',maxNStarsGalaxia
        print 'min(nStarsFac) = ',minNStarsFac, ', max(nStarsFac) = ',maxNStarsFac

        if len(Galaxia.pixels) != len(nStarsGaia):
            print 'ERROR: lengths of pixels(=',len(Galaxia.pixels),') != length of nStarsGaia(=',len(nStarsGaia),')'

        recsGaia = []
        recsGalaxia = []
        recsFac = []
        redGreen = self.getRedGreenPalette()
        edgeColor = 'None'

        faceColorsGaia = [redGreen[int((len(redGreen)-1) * i / maxNStarsGaia)] for i in nStarsGaia]

        faceColorsGalaxia = [redGreen[int((len(redGreen)-1) * i / maxNStarsGalaxia)] for i in nStarsGalaxia]

#        maxNStarsFac = 2.0
#        nStarsFac = np.where(nStarsFac > maxNStarsFac, maxNStarsFac, nStarsFac)
        nStarsFac[np.isnan(nStarsFac)] = maxNStarsFac
        nStarsFac[np.isinf(nStarsFac)] = maxNStarsFac
        colorIndex = [int((len(redGreen)-1.0) * i / maxNStarsFac) for i in nStarsFac]
        faceColorsFac = [redGreen[i] for i in colorIndex]

        for id in pixelIds:
            recsGaia.append(
                Rectangle(
                    (Galaxia.pixels[id].xLow, Galaxia.pixels[id].yLow),   # (x,y)
                     Galaxia.pixels[id].xHigh - Galaxia.pixels[id].xLow,          # width
                     Galaxia.pixels[id].yHigh - Galaxia.pixels[id].yLow,          # height
                )
            )

            recsGalaxia.append(
                Rectangle(
                    (Galaxia.pixels[id].xLow, Galaxia.pixels[id].yLow),   # (x,y)
                     Galaxia.pixels[id].xHigh - Galaxia.pixels[id].xLow,          # width
                     Galaxia.pixels[id].yHigh - Galaxia.pixels[id].yLow,          # height
                )
            )

            recsFac.append(
                Rectangle(
                    (Galaxia.pixels[id].xLow, Galaxia.pixels[id].yLow),   # (x,y)
                     Galaxia.pixels[id].xHigh - Galaxia.pixels[id].xLow,          # width
                     Galaxia.pixels[id].yHigh - Galaxia.pixels[id].yLow,          # height
                )
            )
        pcGaia = PatchCollection(recsGaia, facecolors=faceColorsGaia, edgecolors=edgeColor)
        pcGalaxia = PatchCollection(recsGalaxia, facecolors=faceColorsGalaxia, edgecolors=edgeColor)
        pcFac = PatchCollection(recsFac, facecolors=faceColorsFac, edgecolors=edgeColor)

        xMin = self.ham.lonLatToXY(-179.999, 0).x
        yMin = self.ham.lonLatToXY(0, -89.999).y

        if True:
            fig, ax = plt.subplots(3, sharex=True, sharey=True, figsize=(7, 9.5))

            ax[0].add_collection(pcGaia)
            ax[0].set_title('Gaia')

            ax[1].add_collection(pcGalaxia)
            ax[1].set_title('Galaxia')

            ax[2].add_collection(pcFac)
            ax[2].set_title('nStarsGalaxia / nStarsGaia < 2.0')

            plt.axis([xMin, -xMin, yMin, -yMin])
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

    ham = hammer.Hammer()
    Galaxia.pixels = ham.getPixels()
    Galaxia.whichOne = 'gaiaTgas'

    # remove existing lock files
    for f in glob('/var/lock/*.lock'):
        os.remove(f)

    if False:
        # rename existing outFile
        if os.path.isfile(gal.getOutFileName()):
            shutil.move(gal.getOutFileName(), gal.getOutFileName()+'.bak')

        with open(gal.getOutFileName(), 'w') as f:
            f.write('#PixelId Galaxia Gaia\n')

        p = Pool(processes=12)
        pix = range(len(Galaxia.pixels))
        p.map(processGalaxia, pix)
        p.close()

    gal.plotResult()

if __name__ == '__main__':
    main(sys.argv)
