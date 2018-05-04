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

import csvData
import csvFree
import galcomp
import hammer

class CountStars(object):
    ham = hammer.Hammer()
    pixels = []
    whichOne = 'gaiaTgas'

    def __init__(self):
        """ do nothing """

    def getOutFileNameGaia(self):
        if CountStars.whichOne == "gaiaTgas":
            return '/Volumes/yoda/azuri/data/gaia-tgas/nStarsPerPixel.dat'
        elif CountStars.whichOne == "gaia":
            return '/Volumes/yoda/azuri/data/gaia/nStarsPerPixel.dat'
        else:
            print 'CountStars.getOutFileName: ERROR: CountStars.whichOne(=',CountStars.whichOne,') not found in [gaia, gaiaTgas]'
            STOP

    def getOutFileNameGalaxia(self):
        return '/Volumes/yoda/azuri/data/galaxia/nStarsPerPixel.dat'

    def countStars(self, iPixel):
        print 'iPixel = ',iPixel
        galcomp.countStars(CountStars.pixels, iPixel, self.getOutFileNameGaia(), CountStars.whichOne)
        galcomp.countStars(CountStars.pixels, iPixel, self.getOutFileNameGalaxia(), 'galaxia')

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
        dataGaia = csvFree.readCSVFile(self.getOutFileNameGaia())
        print 'dataGaia.header = ',dataGaia.header
        dataGalaxia = csvFree.readCSVFile(self.getOutFileNameGalaxia())

        pixelIds = csvFree.convertStringVectorToUnsignedVector(dataGaia.getData('PixelId'))

        nStarsGalaxia = np.asarray(csvFree.convertStringVectorToDoubleVector(dataGalaxia.getData('Galaxia')))
        maxNStarsGalaxia = max(nStarsGalaxia)
        minNStarsGalaxia = min(nStarsGalaxia)

        nStarsGaia = np.asarray(csvFree.convertStringVectorToDoubleVector(dataGaia.getData('Gaia')))
        maxNStarsGaia = max(nStarsGaia)
        minNStarsGaia = min(nStarsGaia)



        nStarsFac = nStarsGalaxia / nStarsGaia
        maxNStarsFac = max(nStarsFac[np.isfinite(nStarsFac)])
        minNStarsFac = min(nStarsFac[np.isfinite(nStarsFac)])
        nStarsFac[np.isnan(nStarsFac)] = maxNStarsFac
        nStarsFac[np.isinf(nStarsFac)] = maxNStarsFac

        print 'min(nStarsGaia) = ',minNStarsGaia, ', max(nStarsGaia) = ',maxNStarsGaia
        print 'min(nStarsGalaxia) = ',minNStarsGalaxia, ', max(nStarsGalaxia) = ',maxNStarsGalaxia
        print 'min(nStarsFac) = ',minNStarsFac, ', max(nStarsFac) = ',maxNStarsFac

        if len(CountStars.pixels) != len(nStarsGaia):
            print 'ERROR: lengths of pixels(=',len(CountStars.pixels),') != length of nStarsGaia(=',len(nStarsGaia),')'

        recsGaia = []
        recsGalaxia = []
        recsFac = []
        redGreen = self.getRedGreenPalette()
        edgeColor = 'None'

        faceColorsGaia = [redGreen[int((len(redGreen)-1) * i / maxNStarsGaia)] for i in nStarsGaia]

        maxNStarsGalaxia = maxNStarsGalaxia / 10.0
        nStarsGalaxia = np.where(nStarsGalaxia > maxNStarsGalaxia, maxNStarsGalaxia, nStarsGalaxia)
        faceColorsGalaxia = [redGreen[int((len(redGreen)-1) * i / maxNStarsGalaxia)] for i in nStarsGalaxia]

        maxNStarsFac = 1.0#maxNStarsFac / 10.0
        nStarsFac = np.where(nStarsFac > maxNStarsFac, maxNStarsFac, nStarsFac)
        colorIndex = [int((len(redGreen)-1.0) * i / maxNStarsFac) for i in nStarsFac]
        faceColorsFac = [redGreen[i] for i in colorIndex]

        for id in pixelIds:
            recsGaia.append(
                Rectangle(
                    (CountStars.pixels[id].xLow, CountStars.pixels[id].yLow),   # (x,y)
                     CountStars.pixels[id].xHigh - CountStars.pixels[id].xLow,          # width
                     CountStars.pixels[id].yHigh - CountStars.pixels[id].yLow,          # height
                )
            )

            recsGalaxia.append(
                Rectangle(
                    (CountStars.pixels[id].xLow, CountStars.pixels[id].yLow),   # (x,y)
                     CountStars.pixels[id].xHigh - CountStars.pixels[id].xLow,          # width
                     CountStars.pixels[id].yHigh - CountStars.pixels[id].yLow,          # height
                )
            )

            recsFac.append(
                Rectangle(
                    (CountStars.pixels[id].xLow, CountStars.pixels[id].yLow),   # (x,y)
                     CountStars.pixels[id].xHigh - CountStars.pixels[id].xLow,          # width
                     CountStars.pixels[id].yHigh - CountStars.pixels[id].yLow,          # height
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

def processCountStars(iPix):
    gal = CountStars()
    gal.countStars(iPix)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """

    gal = CountStars()

    ham = hammer.Hammer()
    CountStars.pixels = ham.getPixels()
    CountStars.whichOne = 'gaiaTgas'

    # remove existing lock files
    for f in glob('/var/lock/*.lock'):
        os.remove(f)

    if True:
        # rename existing outFile
        if os.path.isfile(gal.getOutFileNameGaia()):
            shutil.move(gal.getOutFileNameGaia(), gal.getOutFileNameGaia()+'.bak')
        if os.path.isfile(gal.getOutFileNameGalaxia()):
            shutil.move(gal.getOutFileNameGalaxia(), gal.getOutFileNameGalaxia()+'.bak')

        with open(gal.getOutFileNameGaia(), 'w') as f:
            f.write('PixelId,nStars\n')
        with open(gal.getOutFileNameGalaxia(), 'w') as f:
            f.write('PixelId,nStars\n')

        p = Pool(processes=12)
        pix = range(len(CountStars.pixels))
        p.map(processCountStars, pix)
        p.close()

    gal.plotResult()

if __name__ == '__main__':
    main(sys.argv)
