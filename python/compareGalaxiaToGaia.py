import numpy as np
import os

import csvFree,csvData
from gaiaApplyCoordTrafo import process
from hammer import Hammer,XY,Pixel

galaxiaFileNameGen = '/Volumes/discovery/azuri/data/galaxia/ubv_Vlt21.5_1.0/xy/galaxia_%0.6f-%0.6f_%0.6f-%0.6f.csv'
gaiaFileNameGen = '/Volumes/discovery/azuri/data/gaia/dr2/xy/GaiaSource_%0.6f-%0.6f_%0.6f-%0.6f.csv'
fNameOut = '/Users/azuri/daten/illume_research/martin/results.csv'
iPixel = 1001

withDwarfs = True

ham = Hammer()
pixels = ham.getPixelsSmallTowardsCenter()
pixelsOld = ham.getPixels()
print('len(pixels) = ',len(pixels))
print('len(pixelsOld) = ',len(pixelsOld))

minGBP,maxGBP = [-100.,25.]#getGBPLimits(100)
print('minGBP = ',minGBP,', maxGBP = ',maxGBP)

print('we have ',len(pixels),' pixels in the Hammer projection')
print('pixels[iPixel] = ',pixels[iPixel])
print('pixels[iPixel].xLow = ',pixels[iPixel].xLow)


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

def compareNumberOfStars():

    lastPix = -1
    pixelsDone = []
    with open(fNameOut,'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
#        if len(lines) > 1:
#            print('lines[',len(lines)-1,'] = ',lines[len(lines)-1])
            lastPix = int(line.split(',')[0])
            pixelsDone.append(lastPix)
#            print('lastPix = ',lastPix)
    if lastPix == -1:
        with open(fNameOut,'w') as f:
            f.write('iPixel,pixelxMin,pixelXMax,pixelYMin,pixelYMax,nStarsGaia,nStarsGalaxia\n')

    if True:
        allPix = np.arange(1,len(pixels),1)
        print('allPix = ',type(allPix),': ',allPix)
        np.random.shuffle(allPix)
        print('allPix = ',type(allPix),': ',allPix)
        for iPixel in allPix:#lastPix+1,len(pixels),1)):
            if iPixel not in pixelsDone:
                print(' ')
                print('running on pixel ',iPixel)
                galaxiaFileName = galaxiaFileNameGen % (pixels[iPixel].xLow, pixels[iPixel].xHigh, pixels[iPixel].yLow, pixels[iPixel].yHigh)
                print('galaxiaFileName = '+galaxiaFileName)
                if not os.path.isfile(galaxiaFileName):
                    print('ERROR: galaxiaFileName '+galaxiaFileName+' does not exist')
                    STOP

                gaiaFileName = gaiaFileNameGen % (pixels[iPixel].xLow, pixels[iPixel].xHigh, pixels[iPixel].yLow, pixels[iPixel].yHigh)
                print('gaiaFileName = '+gaiaFileName)
                hasXYZ = False

                galaxiaData = csvFree.readCSVFile(galaxiaFileName)

    #            print('galaxiaData.header = ',galaxiaData.header)
    #            print('gaiaData.header = ',gaiaData.header)

    #            print('galaxiaData.size() = ',galaxiaData.size())
    #            print('gaiaData.size() = ',gaiaData.size())

                #logg = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('grav')))
    #            print('surface gravities are ',logg)
                cond = np.asarray(np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('grav'))) < 3.5)
                giants = cond.nonzero()[0]
                print('giants = ',giants)
                print('found ',len(giants),' giants in galaxiaData')
                if withDwarfs:
                    dwarfs = np.invert(cond).nonzero()[0]#np.where(logg >= 3.5)[0]
                    print('dwarfs = ',dwarfs)
        #            STOP
                    print('found ',len(dwarfs),' dwarfs in galaxiaData')
                cond = None

                csvGiants = doMagTrafoGiants(galaxiaData,giants)
                if withDwarfs:
                    csvDwarfs = doMagTrafoDwarfs(galaxiaData,dwarfs)

                galaxiaData = csvGiants
                if withDwarfs:
                    galaxiaData.append(csvDwarfs)
    #            print('galaxiaData.header = ',galaxiaData.header)
    #            print('galaxiaData.size() = ',galaxiaData.size())

                gbp = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('G_BP')))
                galaxiaData = None
                maxGBPGalaxia = np.max(gbp)
                print('maxGBPGalaxia = ',maxGBPGalaxia)
#                print('maxGBP = ',maxGBP)
                goodStars = np.where(gbp <= maxGBP)
                gbp = None
                print('goodStars[0] = ',goodStars[0])
                nGoodStarsGalaxia = len(goodStars[0])
                goodStars = None

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
                if not withDwarfs:
                    logg = np.asarray(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('rv_template_logg')))
                    giants = np.where(logg < 3.5)[0]
                    gbp = np.asarray(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('phot_bp_mean_mag')))[giants]
                    gbp = np.where(gbp <= maxGBPGalaxia)[0]
                    gaiaDataSize = len(giants)
                else:
                    gbp = csvFree.convertStringVectorToDoubleVector(gaiaData.getData('phot_bp_mean_mag'))
                    gbp = np.where(gbp <= maxGBPGalaxia)[0]
                    gaiaDataSize = gbp.size()
#                goodStars = np.where(gbp <= maxGBP)
                gbp = None
#                print('goodStars[0] = ',goodStars[0])
#                nGoodStarsGalaxia = len(goodStars[0])
                goodStars = None
                gaiaData = None
                print('found ',nGoodStarsGalaxia,' stars in magnitude limits in Galaxia and ',gaiaDataSize,' stars in GAIA')

                with open(fNameOut,'a') as f:
                    f.write('%d,%.6f,%.6f,%.6f,%.6f,%d,%d\n' % (iPixel,pixels[iPixel].xLow,pixels[iPixel].xHigh,pixels[iPixel].yLow,pixels[iPixel].yHigh,gaiaDataSize,nGoodStarsGalaxia))

def splitPixelFile(pix):
    oldGalaxiaFileName = galaxiaFileNameGen % (pix.xLow, pix.xHigh, pix.yLow, pix.yHigh)
    print('oldGalaxiaFileName = <'+oldGalaxiaFileName+'>')
    if not os.path.isfile(oldGalaxiaFileName):
        print('ERROR: oldGalaxiaFileName '+oldGalaxiaFileName+' does not exist')
        STOP
    oldGaiaFileName = gaiaFileNameGen % (pix.xLow, pix.xHigh, pix.yLow, pix.yHigh)
    print('oldGaiaFileName = <'+oldGaiaFileName+'>')
    if not os.path.isfile(oldGaiaFileName):
        oldGaiaFileName = oldGaiaFileName[:-4]+'_xyz.csv'
        if not os.path.isfile(oldGaiaFileName):
            print('oldGaiaFileName = '+oldGaiaFileName+' does not exist')
            STOP

    newPixels = []
    xyLL = XY(pix.xLow + 0.0000001, pix.yLow + 0.0000001)
    xyLR = XY(pix.xHigh - 0.0000001, pix.yLow + 0.0000001)
    xyUL = XY(pix.xLow + 0.0000001, pix.yHigh - 0.0000001)
    xyUR = XY(pix.xHigh - 0.0000001, pix.yHigh - 0.0000001)
    for p in pixels:
        if p.isInside(xyLL) or p.isInside(xyLR) or p.isInside(xyUL) or p.isInside(xyUR):
            newPixels.append(p)
            print('pixel ',p,' contained inside pixel ',pix)
    if len(newPixels) != 4:
        print('ERROR: found ',len(newPixels),' instead of 4')
        STOP
    for iRun in [0,1]:
        if iRun == 0:
            oldFileName = oldGalaxiaFileName
            newFileNames = []
            for p in newPixels:
                newFileNames.append(galaxiaFileNameGen % (p.xLow, p.xHigh, p.yLow, p.yHigh))
        else:
            oldFileName = oldGaiaFileName
            newFileNames = []
            for p in newPixels:
                newFileNames.append(gaiaFileNameGen % (p.xLow, p.xHigh, p.yLow, p.yHigh))
        with open(oldFileName,'r') as f:
            allLines = f.readlines()
        header = allLines[0]
        dataLines = allLines[1:]
        csvData = csvFree.readCSVFile(oldFileName)
        with open(newFileNames[0],'w') as nf1:
            nf1.write(header)
            with open(newFileNames[1],'w') as nf2:
                nf2.write(header)
                with open(newFileNames[2],'w') as nf3:
                    nf3.write(header)
                    with open(newFileNames[3],'w') as nf4:
                        nf4.write(header)
                        for i in range(csvData.size()):
                            xy = XY(float(csvData.getData('hammerX',i)),float(csvData.getData('hammerY',i)))
                            for iPix in range(len(newPixels)):
                                if newPixels[iPix].isInside(xy):
                                    if iPix == 0:
                                        nf1.write(dataLines[i])
                                    elif iPix == 1:
                                        nf2.write(dataLines[i])
                                    elif iPix == 2:
                                        nf3.write(dataLines[i])
                                    else:
                                        nf4.write(dataLines[i])

        print('finished creating file '+newFileNames[0])
        print('finished creating file '+newFileNames[1])
        print('finished creating file '+newFileNames[2])
        print('finished creating file '+newFileNames[3])

def compareProperMotions():
    lastPix = -1
    pixelsDone = []
    if os.path.isfile(fNameOut):
        with open(fNameOut,'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
    #        if len(lines) > 1:
    #            print('lines[',len(lines)-1,'] = ',lines[len(lines)-1])
                lastPix = int(line.split(',')[0])
                pixelsDone.append(lastPix)
    print('pixelsDone = ',pixelsDone)
    if len(pixelsDone) == 0:
        with open(fNameOut,'w') as f:
            f.write('iPixel,pixelxMin,pixelXMax,pixelYMin,pixelYMax,nStarsGaia,nStarsGaiaDwarfs,nStarsGaiaGiants,nGoodStarsGalaxia,nGoodStarsGalaxiaDwarfs,nGoodStarsGalaxiaGiants,mean_pm_x_gaia,sdev_pm_x_gaia,mean_pm_y_gaia,sdev_pm_y_gaia,mean_pm_z_gaia,sdev_pm_z_gaia,mean_pm_x_gaiaDwarfs,sdev_pm_x_gaiaDwarfs,mean_pm_y_gaiaDwarfs,sdev_pm_y_gaiaDwarfs,mean_pm_z_gaiaDwarfs,sdev_pm_z_gaiaDwarfs,mean_pm_x_gaiaGiants,sdev_pm_x_gaiaGiants,mean_pm_y_gaiaGiants,sdev_pm_y_gaiaGiants,mean_pm_z_gaiaGiants,sdev_pm_z_gaiaGiants,mean_pm_x_galaxia,sdev_pm_x_galaxia,mean_pm_y_galaxia,sdev_pm_y_galaxia,mean_pm_z_galaxia,sdev_pm_z_galaxia,mean_pm_x_gaiaDwarfs,sdev_pm_x_gaiaDwarfs,mean_pm_y_gaiaDwarfs,sdev_pm_y_gaiaDwarfs,mean_pm_z_gaiaDwarfs,sdev_pm_z_gaiaDwarfs,mean_pm_x_gaiaGiants,sdev_pm_x_gaiaGiants,mean_pm_y_gaiaGiants,sdev_pm_y_gaiaGiants,mean_pm_z_gaiaGiants,sdev_pm_z_gaiaGiants\n')
    iPix = np.arange(0,len(pixels),1)
    np.random.shuffle(iPix)
    for iPixel in iPix:#np.arange(len(pixels)-1,0,-1):
        if iPixel not in pixelsDone:
            print(' ')
            print('running on pixel ',iPixel)
            minCoord = np.min([abs(pixels[iPixel].xLow), abs(pixels[iPixel].xHigh), abs(pixels[iPixel].yLow), abs(pixels[iPixel].yHigh)])
            if minCoord > 0.05:
                galaxiaFileName = galaxiaFileNameGen % (pixels[iPixel].xLow, pixels[iPixel].xHigh, pixels[iPixel].yLow, pixels[iPixel].yHigh)
                print('galaxiaFileName = '+galaxiaFileName)
                if not os.path.isfile(galaxiaFileName):
                    print('ERROR: galaxiaFileName '+galaxiaFileName+' does not exist')
                    xy = XY(pixels[iPixel].xLow+0.0000001,pixels[iPixel].yLow+0.0000001)
                    for tmpPix in pixelsOld:
                        if tmpPix.isInside(xy):
                            print('found old pixel containing xy = ',xy)
                            splitPixelFile(tmpPix)
    #                STOP

                galaxiaData = csvFree.readCSVFile(galaxiaFileName)

    #            print('galaxiaData.header = ',galaxiaData.header)
    #            print('gaiaData.header = ',gaiaData.header)

    #            print('galaxiaData.size() = ',galaxiaData.size())
    #            print('gaiaData.size() = ',gaiaData.size())

                #logg = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('grav')))
    #            print('surface gravities are ',logg)
                cond = np.asarray(np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('grav'))) < 3.5)
                giants = cond.nonzero()[0]
                print('giants = ',giants)
                print('found ',len(giants),' giants in galaxiaData')
                dwarfs = np.invert(cond).nonzero()[0]#np.where(logg >= 3.5)[0]
                print('dwarfs = ',dwarfs)
    #            STOP
                print('found ',len(dwarfs),' dwarfs in galaxiaData')
                cond = None

                csvGiants = doMagTrafoGiants(galaxiaData,giants)
                csvDwarfs = doMagTrafoDwarfs(galaxiaData,dwarfs)

                galaxiaData = csvGiants
                if withDwarfs:
                    galaxiaData.append(csvDwarfs)
    #            print('galaxiaData.header = ',galaxiaData.header)
    #            print('galaxiaData.size() = ',galaxiaData.size())

                if galaxiaData.size() == 0:
                    nGoodStarsGalaxia = 0
                    mean_pm_x_galaxia = float("NaN")
                    sdev_pm_x_galaxia = float("NaN")
                    mean_pm_y_galaxia = float("NaN")
                    sdev_pm_y_galaxia = float("NaN")
                    mean_pm_z_galaxia = float("NaN")
                    sdev_pm_z_galaxia = float("NaN")
                    nGoodStarsGalaxiaDwarfs = 0
                    mean_pm_x_galaxiaDwarfs = float("NaN")
                    sdev_pm_x_galaxiaDwarfs = float("NaN")
                    mean_pm_y_galaxiaDwarfs = float("NaN")
                    sdev_pm_y_galaxiaDwarfs = float("NaN")
                    mean_pm_z_galaxiaDwarfs = float("NaN")
                    sdev_pm_z_galaxiaDwarfs = float("NaN")
                    nGoodStarsGalaxiaGiants = 0
                    mean_pm_x_galaxiaGiants = float("NaN")
                    sdev_pm_x_galaxiaGiants = float("NaN")
                    mean_pm_y_galaxiaGiants = float("NaN")
                    sdev_pm_y_galaxiaGiants = float("NaN")
                    mean_pm_z_galaxiaGiants = float("NaN")
                    sdev_pm_z_galaxiaGiants = float("NaN")
                else:
                    gbp = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('G_BP')))
                    print('galaxia: gbp = ',gbp)
                    nStarsGalaxia = gbp.shape[0]
                    goodStars = np.where(gbp <= maxGBP)
                    minGBPGalaxia = np.min(gbp)
                    maxGBPGalaxia = np.max(gbp)
                    print('galaxia: maxGBP = ',maxGBP,', minGBPGalaxia = ',minGBPGalaxia,', maxGBPGalaxia = ',maxGBPGalaxia)
                    print('galaxia: goodStars[0] = ',goodStars[0])
                    nGoodStarsGalaxia = len(goodStars[0])

                    pmVec = csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('px'))
                    mean_pm_x_galaxia = np.mean(pmVec)
                    sdev_pm_x_galaxia = np.std(pmVec)
                    pmVec = csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('py'))
                    mean_pm_y_galaxia = np.mean(pmVec)
                    sdev_pm_y_galaxia = np.std(pmVec)
                    pmVec = csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('pz'))
                    mean_pm_z_galaxia = np.mean(pmVec)
                    sdev_pm_z_galaxia = np.std(pmVec)
                    pmVec = None
                    galaxiaData = None

                    gbpDwarfs = np.array(csvFree.convertStringVectorToDoubleVector(csvDwarfs.getData('G_BP')))
                    print('galaxia: gbpDwarfs = ',gbpDwarfs)
                    nStarsGalaxiaDwarfs = gbpDwarfs.shape[0]
                    goodStarsDwarfs = np.where(gbpDwarfs <= maxGBP)
                    minGBPGalaxiaDwarfs = np.min(gbpDwarfs)
                    maxGBPGalaxiaDwarfs = np.max(gbpDwarfs)
                    print('galaxia: maxGBP = ',maxGBP,', minGBPGalaxiaDwarfs = ',minGBPGalaxiaDwarfs,', maxGBPGalaxia = ',maxGBPGalaxiaDwarfs)
                    print('galaxia: goodStarsDwarfs[0] = ',goodStarsDwarfs[0])
                    nGoodStarsGalaxiaDwarfs = len(goodStarsDwarfs[0])

                    pmVec = csvFree.convertStringVectorToDoubleVector(csvDwarfs.getData('px'))
                    mean_pm_x_galaxiaDwarfs = np.mean(pmVec)
                    sdev_pm_x_galaxiaDwarfs = np.std(pmVec)
                    pmVec = csvFree.convertStringVectorToDoubleVector(csvDwarfs.getData('py'))
                    mean_pm_y_galaxiaDwarfs = np.mean(pmVec)
                    sdev_pm_y_galaxiaDwarfs = np.std(pmVec)
                    pmVec = csvFree.convertStringVectorToDoubleVector(csvDwarfs.getData('pz'))
                    mean_pm_z_galaxiaDwarfs = np.mean(pmVec)
                    sdev_pm_z_galaxiaDwarfs = np.std(pmVec)
                    pmVec = None
                    csvDwarfs = None

                    gbpGiants = np.array(csvFree.convertStringVectorToDoubleVector(csvGiants.getData('G_BP')))
                    print('galaxia: gbpGiants = ',gbpGiants)
                    nStarsGalaxiaGiants = gbpGiants.shape[0]
                    goodStarsGiants = np.where(gbpGiants <= maxGBP)
                    minGBPGalaxiaGiants = np.min(gbpGiants)
                    maxGBPGalaxiaGiants = np.max(gbpGiants)
                    print('galaxia: maxGBP = ',maxGBP,', minGBPGalaxiaGiants = ',minGBPGalaxiaGiants,', maxGBPGalaxiaGiants = ',maxGBPGalaxiaGiants)
                    print('galaxia: goodStarsGiants[0] = ',goodStarsGiants[0])
                    nGoodStarsGalaxiaGiants = len(goodStarsGiants[0])

                    pmVec = csvFree.convertStringVectorToDoubleVector(csvGiants.getData('px'))
                    mean_pm_x_galaxiaGiants = np.mean(pmVec)
                    sdev_pm_x_galaxiaGiants = np.std(pmVec)
                    pmVec = csvFree.convertStringVectorToDoubleVector(csvGiants.getData('py'))
                    mean_pm_y_galaxiaGiants = np.mean(pmVec)
                    sdev_pm_y_galaxiaGiants = np.std(pmVec)
                    pmVec = csvFree.convertStringVectorToDoubleVector(csvGiants.getData('pz'))
                    mean_pm_z_galaxiaGiants = np.mean(pmVec)
                    sdev_pm_z_galaxiaGiants = np.std(pmVec)
                    pmVec = None
                    csvGiants = None

                goodStars = None

                gaiaFileName = gaiaFileNameGen % (pixels[iPixel].xLow, pixels[iPixel].xHigh, pixels[iPixel].yLow, pixels[iPixel].yHigh)
                print('gaiaFileName = '+gaiaFileName)
                hasXYZ = False
                if not os.path.isfile(gaiaFileName):
                    hasXYZ = True
                    gaiaFileName = gaiaFileName[:-4]+'_xyz.csv'
                    print('gaiaFileName = '+gaiaFileName)
                    if not os.path.isfile(gaiaFileName):
                        print('ERROR: gaiaFileName '+gaiaFileName+' does not exist')
                        xy = XY(pixels[iPixel].xLow+0.0000001,pixels[iPixel].yLow+0.0000001)
                        for tmpPix in pixelsOld:
                            if tmpPix.isInside(xy):
                                print('found old pixel containing xy = ',xy)
                                splitPixelFile(tmpPix)
                        gaiaFileName = gaiaFileNameGen % (pixels[iPixel].xLow, pixels[iPixel].xHigh, pixels[iPixel].yLow, pixels[iPixel].yHigh)
                        hasXYZ = False
                        if not os.path.isfile(gaiaFileName):
                            gaiaFileName = gaiaFileName[:-4]+'_xyz.csv'
                            hasXYZ = True
                            print('gaiaFileName = '+gaiaFileName)
                            if not os.path.isfile(gaiaFileName):
                                print('ERROR: gaiaFileName '+gaiaFileName+' does not exist')
                                STOP
                    gaiaData = csvFree.readCSVFile(gaiaFileName)
                if not hasXYZ:
                    gaiaData = process(gaiaFileName)

                if gaiaData.size() == 0:
                    nStarsGaia = 0
                    mean_pm_x_gaia = float("NaN")
                    sdev_pm_x_gaia = float("NaN")
                    mean_pm_y_gaia = float("NaN")
                    sdev_pm_y_gaia = float("NaN")
                    mean_pm_z_gaia = float("NaN")
                    sdev_pm_z_gaia = float("NaN")
                    nStarsGaiaDwarfs = 0
                    mean_pm_x_gaiaDwarfs = float("NaN")
                    sdev_pm_x_gaiaDwarfs = float("NaN")
                    mean_pm_y_gaiaDwarfs = float("NaN")
                    sdev_pm_y_gaiaDwarfs = float("NaN")
                    mean_pm_z_gaiaDwarfs = float("NaN")
                    sdev_pm_z_gaiaDwarfs = float("NaN")
                    nStarsGaiaGiants = 0
                    mean_pm_x_gaiaGiants  = float("NaN")
                    sdev_pm_x_gaiaGiants  = float("NaN")
                    mean_pm_y_gaiaGiants  = float("NaN")
                    sdev_pm_y_gaiaGiants  = float("NaN")
                    mean_pm_z_gaiaGiants  = float("NaN")
                    sdev_pm_z_gaiaGiants  = float("NaN")
                else:
                    gbp = np.asarray(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('phot_bp_mean_mag')))
                    print('gaia gbp = ',gbp)
                    print('min(gbp) = ',np.min(gbp),', max(gbp) = ',np.max(gbp))
                    inGBPLimits = np.where(gbp <= maxGBPGalaxia)[0]
                    print('gbp.shape[0] = ',gbp.shape[0],': inGBPLimits = ',inGBPLimits.shape[0],': ',inGBPLimits)

                    cond = np.asarray(np.array(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('rv_template_logg')))[inGBPLimits] < 3.5)
                    gaiaGiants = cond.nonzero()[0]
                    csvGaiaGiants = csvData.CSVData()
                    csvGaiaGiants.header = gaiaData.header
                    for i in range(len(gaiaGiants)):
                        csvGaiaGiants.append(gaiaData.getData(inGBPLimits[gaiaGiants[i]]))

                    print('gaiaGiants = ',gaiaGiants)
                    print('found ',len(gaiaGiants),' giants in gaiaData')
                    gaiaDwarfs = np.invert(cond).nonzero()[0]#np.where(logg >= 3.5)[0]
                    csvGaiaDwarfs = csvData.CSVData()
                    csvGaiaDwarfs.header = gaiaData.header
                    for i in range(len(gaiaDwarfs)):
                        csvGaiaDwarfs.append(gaiaData.getData(inGBPLimits[gaiaDwarfs[i]]))
                    #gaiaGiants = np.where(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('rv_template_logg')) < 3.5)[0]

                    nStarsGaia = inGBPLimits.shape[0]
                    nStarsGaiaGiants = len(gaiaGiants)
                    nStarsGaiaDwarfs = len(gaiaDwarfs)
                    print('found ',nGoodStarsGalaxia,' stars out of ',nStarsGalaxia,' in magnitude limits in Galaxia and ',nStarsGaia,' stars in GAIA out of ',gbp.shape[0])
                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('pmXGal')))[inGBPLimits]
                    mean_pm_x_gaia = np.mean(pmVec)
                    sdev_pm_x_gaia = np.std(pmVec)
                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('pmYGal')))[inGBPLimits]
                    mean_pm_y_gaia = np.mean(pmVec)
                    sdev_pm_y_gaia = np.std(pmVec)
                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(gaiaData.getData('pmZGal')))[inGBPLimits]
                    mean_pm_z_gaia = np.mean(pmVec)
                    sdev_pm_z_gaia = np.std(pmVec)
                    pmVec = None
                    gaiaData = None

                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(csvGaiaDwarfs.getData('pmXGal')))
                    mean_pm_x_gaiaDwarfs = np.mean(pmVec)
                    sdev_pm_x_gaiaDwarfs = np.std(pmVec)
                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(csvGaiaDwarfs.getData('pmYGal')))
                    mean_pm_y_gaiaDwarfs = np.mean(pmVec)
                    sdev_pm_y_gaiaDwarfs = np.std(pmVec)
                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(csvGaiaDwarfs.getData('pmZGal')))
                    mean_pm_z_gaiaDwarfs = np.mean(pmVec)
                    sdev_pm_z_gaiaDwarfs = np.std(pmVec)
                    csvGaiaDwarfs = None

                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(csvGaiaGiants.getData('pmXGal')))
                    mean_pm_x_gaiaGiants = np.mean(pmVec)
                    sdev_pm_x_gaiaGiants = np.std(pmVec)
                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(csvGaiaGiants.getData('pmYGal')))
                    mean_pm_y_gaiaGiants = np.mean(pmVec)
                    sdev_pm_y_gaiaGiants = np.std(pmVec)
                    pmVec = np.asarray(csvFree.convertStringVectorToDoubleVector(csvGaiaGiants.getData('pmZGal')))
                    mean_pm_z_gaiaGiants = np.mean(pmVec)
                    sdev_pm_z_gaiaGiants = np.std(pmVec)
                    csvGaiaGiants = None

                with open(fNameOut,'a') as f:
                    #iPixel,pixelxMin,pixelXMax,pixelYMin,pixelYMax,nStarsGaia,nStarsGaiaDwarfs,nStarsGaiaGiants,nGoodStarsGalaxia,nGoodStarsGalaxiaDwarfs,nGoodStarsGalaxiaGiants,mean_pm_x_gaia,sdev_pm_x_gaia,mean_pm_y_gaia,sdev_pm_y_gaia,mean_pm_z_gaia,sdev_pm_z_gaia,mean_pm_x_gaiaDwarfs,sdev_pm_x_gaiaDwarfs,mean_pm_y_gaiaDwarfs,sdev_pm_y_gaiaDwarfs,mean_pm_z_gaiaDwarfs,sdev_pm_z_gaiaDwarfs,mean_pm_x_gaiaGiants,sdev_pm_x_gaiaGiants,mean_pm_y_gaiaGiants,sdev_pm_y_gaiaGiants,mean_pm_z_gaiaGiants,sdev_pm_z_gaiaGiants,mean_pm_x_galaxia,sdev_pm_x_galaxia,mean_pm_y_galaxia,sdev_pm_y_galaxia,mean_pm_z_galaxia,sdev_pm_z_galaxia,mean_pm_x_gaiaDwarfs,sdev_pm_x_gaiaDwarfs,mean_pm_y_gaiaDwarfs,sdev_pm_y_gaiaDwarfs,mean_pm_z_gaiaDwarfs,sdev_pm_z_gaiaDwarfs,mean_pm_x_gaiaGiants,sdev_pm_x_gaiaGiants,mean_pm_y_gaiaGiants,sdev_pm_y_gaiaGiants,mean_pm_z_gaiaGiants,sdev_pm_z_gaiaGiants
                    f.write('%d,%.6f,%.6f,%.6f,%.6f,%d,%d,%d,%d,%d,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n' 
                            % (iPixel,
                                pixels[iPixel].xLow,
                                pixels[iPixel].xHigh,
                                pixels[iPixel].yLow,
                                pixels[iPixel].yHigh,
                                nStarsGaia,
                                nStarsGaiaDwarfs,
                                nStarsGaiaGiants,
                                nGoodStarsGalaxia,
                                nGoodStarsGalaxiaDwarfs,
                                nGoodStarsGalaxiaGiants,
                                mean_pm_x_gaia,
                                sdev_pm_x_gaia,
                                mean_pm_y_gaia,
                                sdev_pm_y_gaia,
                                mean_pm_z_gaia,
                                sdev_pm_z_gaia,
                                mean_pm_x_gaiaDwarfs,
                                sdev_pm_x_gaiaDwarfs,
                                mean_pm_y_gaiaDwarfs,
                                sdev_pm_y_gaiaDwarfs,
                                mean_pm_z_gaiaDwarfs,
                                sdev_pm_z_gaiaDwarfs,
                                mean_pm_x_gaiaGiants,
                                sdev_pm_x_gaiaGiants,
                                mean_pm_y_gaiaGiants,
                                sdev_pm_y_gaiaGiants,
                                mean_pm_z_gaiaGiants,
                                sdev_pm_z_gaiaGiants,
                                mean_pm_x_galaxia,
                                sdev_pm_x_galaxia,
                                mean_pm_y_galaxia,
                                sdev_pm_y_galaxia,
                                mean_pm_z_galaxia,
                                sdev_pm_z_galaxia,
                                mean_pm_x_galaxiaDwarfs,
                                sdev_pm_x_galaxiaDwarfs,
                                mean_pm_y_galaxiaDwarfs,
                                sdev_pm_y_galaxiaDwarfs,
                                mean_pm_z_galaxiaDwarfs,
                                sdev_pm_z_galaxiaDwarfs,
                                mean_pm_x_galaxiaGiants,
                                sdev_pm_x_galaxiaGiants,
                                mean_pm_y_galaxiaGiants,
                                sdev_pm_y_galaxiaGiants,
                                mean_pm_z_galaxiaGiants,
                                sdev_pm_z_galaxiaGiants
                                ))
                #STOP

if __name__ == '__main__':
#    compareNumberOfStars()
    compareProperMotions()
    if False:
        with open('/Users/azuri/temp/pixels.dat','w') as f:
            i = 0
            for pix in pixels:
                f.write('%.6f %.6f %.6f %.6f\n' % (pix.xLow,pix.xHigh,pix.yLow,pix.yHigh))
                i+=1
        with open('/Users/azuri/temp/pixelsOld.dat','w') as f:
            i = 0
            for pix in pixelsOld:
                f.write('%.6f %.6f %.6f %.6f\n' % (pix.xLow,pix.xHigh,pix.yLow,pix.yHigh))
                i+=1
    if False:
        for pixOld in pixelsOld:
            nPixFound = 0
            for pix in pixels:
                if (pixOld.xLow == pix.xLow) and (pixOld.xHigh == pix.xHigh) and (pixOld.yLow == pix.yLow) and (pixOld.yHigh == pix.yHigh):
    #                print('pixels in pixelsOld and not in pixels = ',pix)
                    nPixFound += 1
            if nPixFound == 0:
                print('did not find pix=',pix,' in pixels')
        for pix in pixels:
            nPixFound = 0
            for pixOld in pixelsOld:
                if (pixOld.xLow == pix.xLow) and (pixOld.xHigh == pix.xHigh) and (pixOld.yLow == pix.yLow) and (pixOld.yHigh == pix.yHigh):
    #                print('pixels in pixelsOld and not in pixels = ',pix)
                    nPixFound += 1
            if nPixFound == 0:
                print('did not find pix=',pix,' in pixelsOld')

        for pix in pixelsOld:
            if (pix.xLow > -0.05) and (pix.xHigh < 0.05) and (pix.yLow > -0.02) and (pix.yHigh < 0.02):
                print('pix = ',pix)
                splitPixelFile(pix)
                STOP
