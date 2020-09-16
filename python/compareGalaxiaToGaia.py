import numpy as np
import os

import csvFree,csvData
from gaiaApplyCoordTrafo import process
from hammer import Hammer,XY,Pixel

galaxiaFileNameGen = '/Volumes/?lhngzZsdf][tr94/azuri/data/galaxia/ubv_Vlt21.5_1.0/xy/galaxia_%0.6f-%0.6f_%0.6f-%0.6f.csv'
gaiaFileNameGen = '/Volumes/work/azuri/data/gaia/dr2/xy/GaiaSource_%0.6f-%0.6f_%0.6f-%0.6f.csv'
fNameOut = '/Users/azuri/daten/illume_research/martin/results.csv'
iPixel = 1001

ham = Hammer()
pixels = ham.getPixelsSmallTowardsCenter()
pixelsOld = ham.getPixels()
print('len(pixels) = ',len(pixels))
print('len(pixelsOld) = ',len(pixelsOld))

minGBP,maxGBP = [0.,25.]#getGBPLimits(100)
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

    if True:
        if lastPix == -1:
            f.write('iPixel,pixelxMin,pixelXMax,pixelYMin,pixelYMax,nStarsGaia,nStarsGalaxia\n')
        for iPixel in np.arange(len(pixels)-1,0,-1):#lastPix+1,len(pixels),1):
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
                gaiaDataSize = gaiaData.size()
                gaiaData = None

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
                galaxiaData.append(csvDwarfs)
    #            print('galaxiaData.header = ',galaxiaData.header)
    #            print('galaxiaData.size() = ',galaxiaData.size())

                gbp = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('G_BP')))
                galaxiaData = None
    #            print('gbp = ',gbp)
                print('maxGBP = ',maxGBP)
                goodStars = np.where(gbp <= maxGBP)
                gbp = None
                print('goodStars[0] = ',goodStars[0])
                nGoodStarsGalaxia = len(goodStars[0])
                goodStars = None
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
            f.write('iPixel,pixelxMin,pixelXMax,pixelYMin,pixelYMax,nStarsGaia,nStarsGalaxia,mean_pm_x_gaia,sdev_pm_x_gaia,mean_pm_y_gaia,sdev_pm_y_gaia,mean_pm_z_gaia,sdev_pm_z_gaia,mean_pm_x_galaxia,sdev_pm_x_galaxia,mean_pm_y_galaxia,sdev_pm_y_galaxia,mean_pm_z_galaxia,sdev_pm_z_galaxia\n')
    for iPixel in np.arange(0,len(pixels),1):#len(pixels)-1,0,-1):
        if iPixel not in pixelsDone:
            print(' ')
            print('running on pixel ',iPixel)
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
            nStarsGaia = gaiaData.size()
            pmVec = csvFree.convertStringVectorToDoubleVector(gaiaData.getData('pmXGal'))
            mean_pm_x_gaia = np.mean(pmVec)
            sdev_pm_x_gaia = np.std(pmVec)
            pmVec = csvFree.convertStringVectorToDoubleVector(gaiaData.getData('pmYGal'))
            mean_pm_y_gaia = np.mean(pmVec)
            sdev_pm_y_gaia = np.std(pmVec)
            pmVec = csvFree.convertStringVectorToDoubleVector(gaiaData.getData('pmZGal'))
            mean_pm_z_gaia = np.mean(pmVec)
            sdev_pm_z_gaia = np.std(pmVec)
            pmVec = None
            gaiaData = None

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
            galaxiaData.append(csvDwarfs)
#            print('galaxiaData.header = ',galaxiaData.header)
#            print('galaxiaData.size() = ',galaxiaData.size())

            gbp = np.array(csvFree.convertStringVectorToDoubleVector(galaxiaData.getData('G_BP')))
#            print('gbp = ',gbp)
            print('maxGBP = ',maxGBP)
            goodStars = np.where(gbp <= maxGBP)
            gbp = None
            print('goodStars[0] = ',goodStars[0])
            nGoodStarsGalaxia = len(goodStars[0])
            print('found ',nGoodStarsGalaxia,' stars in magnitude limits in Galaxia and ',nStarsGaia,' stars in GAIA')

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


            goodStars = None

            with open(fNameOut,'a') as f:
                #iPixel,pixelxMin,pixelXMax,pixelYMin,pixelYMax,nStarsGaia,nStarsGalaxia,mean_pm_x_gaia,sdev_pm_x_gaia,mean_pm_y_gaia,sdev_pm_y_gaia,mean_pm_z_gaia,sdev_pm_z_gaia,mean_pm_x_galaxia,sdev_pm_x_galaxia,mean_pm_y_galaxia,sdev_pm_y_galaxia,mean_pm_z_galaxia,sdev_pm_z_galaxia
                f.write('%d,%.6f,%.6f,%.6f,%.6f,%d,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n' % (iPixel,pixels[iPixel].xLow,pixels[iPixel].xHigh,pixels[iPixel].yLow,pixels[iPixel].yHigh,nStarsGaia,nGoodStarsGalaxia,mean_pm_x_gaia,sdev_pm_x_gaia,mean_pm_y_gaia,sdev_pm_y_gaia,mean_pm_z_gaia,sdev_pm_z_gaia,mean_pm_x_galaxia,sdev_pm_x_galaxia,mean_pm_y_galaxia,sdev_pm_y_galaxia,mean_pm_z_galaxia,sdev_pm_z_galaxia))

if __name__ == '__main__':
    #compareNumberOfStars()
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
