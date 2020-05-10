import numpy as np
import os

import csvFree,csvData
from gaiaApplyCoordTrafo import process
from hammer import Hammer

galaxiaFileNameGen = '/Volumes/?lhngzZsdf][tr94/azuri/data/galaxia/ubv_Vlt21.5_1.0/xy/galaxia_%0.6f-%0.6f_%0.6f-%0.6f.csv'
gaiaFileNameGen = '/Volumes/work/azuri/data/gaia/dr2/xy/GaiaSource_%0.6f-%0.6f_%0.6f-%0.6f.csv'
fNameOut = '/Users/azuri/daten/illume_research/martin/results.csv'
iPixel = 1001

def doMagTrafo(b,v,r,c1,cb,cv,cr):
    gBP = c1 + cb*b + cv*v +cr*r
    return gBP

def doMagTrafoDwarfs(csvDataIn,indices):
    csvDataOut = csvData.CSVData()
    csvDataOut.header = csvDataIn.header
    for i in range(len(indices)):
        csvDataOut.append(csvDataIn.getData(indices[i]))

    b = np.array(csvFree.convertStringVectorToDoubleVector(csvDataOut.getData('ubv_b')))
    v = np.array(csvFree.convertStringVectorToDoubleVector(csvDataOut.getData('ubv_v')))
    r = np.array(csvFree.convertStringVectorToDoubleVector(csvDataOut.getData('ubv_r')))

    c1 = 0.310369
    cb = 0.218680
    cv = 0.631294
    cr = 0.132206

    gBP = doMagTrafo(b,v,r,c1,cb,cv,cr)
    csvDataOut.addColumn('G_BP',gBP)
    return csvDataOut

def doMagTrafoGiants(csvDataIn,indices):
    csvDataOut = csvData.CSVData()
    csvDataOut.header = csvDataIn.header
    for i in range(len(indices)):
        csvDataOut.append(csvDataIn.getData(indices[i]))

    b = np.array(csvFree.convertStringVectorToDoubleVector(csvDataOut.getData('ubv_b')))
    v = np.array(csvFree.convertStringVectorToDoubleVector(csvDataOut.getData('ubv_v')))
    r = np.array(csvFree.convertStringVectorToDoubleVector(csvDataOut.getData('ubv_r')))

    c1 = 0.666924
    cb = 0.185286
    cv = 0.561372
    cr = 0.210602

    gBP = doMagTrafo(b,v,r,c1,cb,cv,cr)
    csvDataOut.addColumn('G_BP',gBP)
    return csvDataOut

def getGBPLimits(nFiles):
    minGBP = 100000.
    maxGBP = 0.
    for i in range(nFiles):
        gaiaFileName = gaiaFileNameGen % (pixels[i].xLow, pixels[i].xHigh, pixels[i].yLow, pixels[i].yHigh)
        print('gaiaFileName = '+gaiaFileName)
        if not os.path.isfile(gaiaFileName):
            gaiaFileName = gaiaFileName[:-4]+'_xyz.csv'
            print('gaiaFileName = '+gaiaFileName)
        gaiaData = csvFree.readCSVFile(gaiaFileName)
        if gaiaData.size() > 0:
            gaiaGBP = np.array(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('phot_bp_mean_mag')))
            maxGaiaGBP = np.amax(gaiaGBP)
            minGaiaGBP = np.amin(gaiaGBP)
            if minGBP > minGaiaGBP:
                minGBP = minGaiaGBP
            if maxGBP < maxGaiaGBP:
                maxGBP = maxGaiaGBP
    return [minGBP,maxGBP]

if __name__ == '__main__':
    ham = Hammer()
    pixels = ham.getPixels()

    minGBP,maxGBP = [0.,25.]#getGBPLimits(100)
    print('minGBP = ',minGBP,', maxGBP = ',maxGBP)

    print('we have ',len(pixels),' pixels in the Hammer projection')
    print('pixels[iPixel] = ',pixels[iPixel])
    print('pixels[iPixel].xLow = ',pixels[iPixel].xLow)

    lastPix = 0
    with open(fNameOut,'r') as f:
        lines = f.readlines()
        print('lines[',len(lines)-1,'] = ',lines[len(lines)-1])
        lastPix = int(lines[len(lines)-1].split(',')[0])
        print('lastPix = ',lastPix)

    with open(fNameOut,'w') as f:
        f.write('iPixel,pixelxMin,pixelXMax,pixelYMin,pixelYMax,nStarsGaia,nStarsGalaxia\n')
        for iPixel in np.arange(lastPix+1,len(pixels),1):
            print(' ')
            print('running on pixel ',iPixel)
            galaxiaFileName = galaxiaFileNameGen % (pixels[iPixel].xLow, pixels[iPixel].xHigh, pixels[iPixel].yLow, pixels[iPixel].yHigh)
            print('galaxiaFileName = '+galaxiaFileName)
            if not os.path.isfile(galaxiaFileName):
                print('ERROR: galaxiaFileName '+galaxiaFileName+' does not exist')
                STOP
            galaxiaData = csvFree.readCSVFile(galaxiaFileName)

            gaiaFileName = gaiaFileNameGen % (pixels[iPixel].xLow, pixels[iPixel].xHigh, pixels[iPixel].yLow, pixels[iPixel].yHigh)
            print('gaiaFileName = '+gaiaFileName)
            hasXYZ = False
            if not os.path.isfile(gaiaFileName):
                hasXYZ = True
                gaiaFileName = gaiaFileName[:-4]+'_xyz.csv'
                print('gaiaFileName = '+gaiaFileName)
                if not os.path.isfile(gaiaFileName):
                    print('ERROR: gaiaFileName '+gaiaFileName+' does not exist')
                    STOP
                gaiaData = csvFree.readCSVFile(gaiaFileName)
            else:
                gaiaData = process(gaiaFileName)


#            print('galaxiaData.header = ',galaxiaData.header)
#            print('gaiaData.header = ',gaiaData.header)

#            print('galaxiaData.size() = ',galaxiaData.size())
#            print('gaiaData.size() = ',gaiaData.size())

            logg = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('grav')))
#            print('surface gravities are ',logg)

            giants = np.where(logg < 3.5)[0]
            print('found ',len(giants),' giants in galaxiaData')
            dwarfs = np.where(logg >= 3.5)[0]
            print('found ',len(dwarfs),' dwarfs in galaxiaData')

            csvGiants = doMagTrafoGiants(galaxiaData,giants)
            csvDwarfs = doMagTrafoDwarfs(galaxiaData,dwarfs)

            galaxiaData = csvGiants
            galaxiaData.append(csvDwarfs)
#            print('galaxiaData.header = ',galaxiaData.header)
#            print('galaxiaData.size() = ',galaxiaData.size())

            gbp = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('G_BP')))
#            print('gbp = ',gbp)
            print('maxGBP = ',maxGBP)
            goodStars = np.where(gbp <= maxGBP)
            print('goodStars[0] = ',goodStars[0])
            nGoodStarsGalaxia = len(goodStars[0])
            print('found ',nGoodStarsGalaxia,' stars in magnitude limits in Galaxia and ',gaiaData.size(),' stars in GAIA')

            f.write('%d,%.6f,%.6f,%.6f,%.6f,%d,%d\n' % (iPixel,pixels[iPixel].xLow,pixels[iPixel].xHigh,pixels[iPixel].yLow,pixels[iPixel].yHigh,gaiaData.size(),nGoodStarsGalaxia))
