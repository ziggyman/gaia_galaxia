from multiprocessing import Pool
import numpy as np
import os
import random

import astropy.units as u
from astropy.coordinates import SkyCoord, Distance
from astropy.time import Time

import csvData
import csvFree
import hammer

from myUtils import hmsToDeg,dmsToDeg,raDecToLonLat,getPixel,angularDistance

import csvFree
import csvData
import hammer
import moveStarsToXY
from gaiaXSimbadImag import readImags#, getStarWithMinDist

ham = hammer.Hammer()
pixels = ham.getPixels()
maxAngularDistance = 5.0

inFileNameSimbadIRoot = '/Volumes/obiwan/azuri/data/simbad/xy/GaiaXSimbadI_%.6f-%.6f_%.6f-%.6f.csv'
inFileNameGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/dr2/xy/GaiaSource_%.6f-%.6f_%.6f-%.6f.csv'

#inFileNameSimbadXGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f.csv'
#inFileNameSimbadXGaiaRootGood = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f_R_phot_rp_mean_mag_rv_template_logg.csv'

outFile = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbadI.csv'
pix = pixels[0]
csvTemp = csvFree.readCSVFile(inFileNameGaiaRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh),',',True)
csvOut = csvData.CSVData()
csvOut.header = csvTemp.header
csvOut.addColumn('SimbadU')
csvOut.addColumn('SimbadB')
csvOut.addColumn('SimbadV')
csvOut.addColumn('SimbadR')
csvOut.addColumn('SimbadI')
csvFree.writeCSVFile(csvOut,outFile)
#STOP
if False:
    simbadData = readImags('/Volumes/obiwan/azuri/data/simbad/simbad_Imag_logg.txt')#simbad_Imag_20000stars.txt')
    print('simbadData.header = ',simbadData.header)
    ra = [float(x) for x in simbadData.getData('RA')]
    dec = [float(x) for x in simbadData.getData('DEC')]
    l = []
    b = []
    hamX = []
    hamY = []
    for iStar in np.arange(0,simbadData.size(),1):
        lon, lat = raDecToLonLat(ra[iStar], dec[iStar])
        l.append(str(lon))
        b.append(str(lat))
        xy = ham.lonLatToXY(lon, lat)
        hamX.append(str(xy.x))
        hamY.append(str(xy.y))
        print(iStar,': ra=',ra[iStar],', dec=',dec[iStar],': lon=',lon,', lat=',lat,', x=',xy.x,', y=',xy.y)
    simbadData.addColumn('l',l)
    simbadData.addColumn('b',b)
    simbadData.addColumn('hammerX',hamX)
    simbadData.addColumn('hammerY',hamY)
    print('simbadData.header = ',simbadData.header)
    csvFree.writeCSVFile(simbadData,'/Volumes/obiwan/azuri/data/simbad/simbad_Imag_logg.csv')

#csvSimbadI = csvFree.readCSVFile('/Volumes/obiwan/azuri/data/gaia/x-match/simbadI/simbad_ImagXGaia.csv.bak',',',False)


def getStarWithMinDist(gaiaData, ra, dec, iStar=0):
    dist = None
    index = -1
#    print('gaiaData.header = ',gaiaData.header)
    gaiaRa = gaiaData.getData('ra')
    gaiaDec = gaiaData.getData('dec')
#    print('gaiaRa = ',gaiaRa,', gaiaDec = ',gaiaDec)
    for i in np.arange(0,gaiaData.size(),1):
#        print('gaiaData.getData(',i,') = ',gaiaData.getData(i))
#        print('gaiaData.getData(parallax,',i,') = ',gaiaData.getData('parallax',i))
        raStar = float(gaiaRa[i])
        decStar = float(gaiaDec[i])
#        print('i = ',i,': raStar = ',raStar,', decStar = ',decStar)#,', pmraStar = ',pmraStar,', pmdecStar = ',pmdecStar)
        if False:#gaiaData.getData('parallax',i) != '':
            parallax = float(gaiaData.getData('parallax',i))
            if parallax < 0.:
                parallax = 0.1
            distance = Distance(parallax=parallax * u.mas)
#            print('distance = ',distance)
#            print("gaiaData.getData('pmra',i) = ",gaiaData.getData('pmra',i))
#            print("gaiaData.getData('pmdec',i) = ",gaiaData.getData('pmdec',i))
            time = Time(float(gaiaData.getData('ref_epoch',i)), format='decimalyear')
#            print('time = ',time)
            c = SkyCoord(ra=raStar*u.degree,
                         dec=decStar*u.degree,
                         distance=distance,
                         pm_ra_cosdec=float(pmraStar) * u.mas/u.yr,
                         pm_dec=float(pmdecStar) * u.mas/u.yr,
                         obstime=time)
#            print('c = ',c)
            c_epoch2000 = c.apply_space_motion(Time('2000-01-01'))
#            print('c_epoch2000 = ',c_epoch2000)
#            print('c_epoch2000 = ',type(c_epoch2000),': ',dir(c_epoch2000),': ',c_epoch2000)
#            print('c_epoch2000.ra = ',type(c_epoch2000.ra),': ',dir(c_epoch2000.ra),': ',c_epoch2000.ra)
#            print('c_epoch2000.ra.deg = ',c_epoch2000.ra.deg)
            thisDist = angularDistance(ra*u.degree, dec*u.degree, c_epoch2000.ra.deg*u.degree, c_epoch2000.dec.deg*u.degree) * 3600.
        else:
#            print('i = ',i,': gaiaData.getData(',i,') = ',gaiaData.getData(i))
#            print('i = ',i,': ra = ',ra,', dec = ',dec,", gaiaData.getData('ra',i) = ",gaiaData.getData('ra',i),", gaiaData.getData('dec',i) = ",gaiaData.getData('dec',i))
#            print('i = ',i,': raStar = ',raStar,', decStar = ',decStar)
            thisDist = angularDistance(ra*u.degree, dec*u.degree, raStar*u.degree, decStar*u.degree) * 3600.
        if (dist is None):
            dist = thisDist
            index = i
        else:
            if dist > thisDist:
                dist = thisDist
                index = i
                print('star ',iStar,': closest star index: ',index,': distance = ',dist)
        if (dist) < 1.:
            return [index, dist]
    return [index, dist]

print('len(pixels) = ',len(pixels))
#for iPix in np.arange(0,len(pixels),1):
def process(iPix):
    pix = pixels[iPix]
    print('pix = ',pix)
    inFileNameSimbad = inFileNameSimbadIRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh)
    print('reading file <'+inFileNameSimbad+'>')
    try:
        csvSimbad = csvFree.readCSVFile(inFileNameSimbad,',',False)
    except Exception &e:
        print('ERROR: exception ',str(e),' occured while reading file <'+inFileNameSimbad+'>')
    print(inFileNameSimbad,': csvSimbad.size() = ',csvSimbad.size())
    if csvSimbad.size() > 0:

        inFileNameGaia = inFileNameGaiaRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh)
        print('reading gaia file <'+inFileNameGaia+'>')
        csvGaia = csvFree.readCSVFile(inFileNameGaia,',',False)
        for iStar in np.arange(0,csvSimbad.size(),1):
            ra = float(csvSimbad.getData('RA',iStar))
            dec = float(csvSimbad.getData('DEC',iStar))
            indexGood, distGood = getStarWithMinDist(csvGaia, ra, dec, iStar)
            print('csvSimbadXGaiaGood: minimum distance good = ',distGood,
                  ': index good = ',indexGood)
            if indexGood >= 0:
                print(inFileNameGaia,': minimum distance good = ',distGood,
                      ': index good = ',indexGood,
                      ', source_id good = ',csvGaia.getData('source_id', indexGood))
    #                inFileNameGaia = inFileNameGaiaRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh)
    #                csvGaia = csvFree.readCSVFile(inFileNameGaia, ',', True)

                    #STOP
                #        print('read ',csvGaia.size(),' stars from')
    #                indexGaia, minDistGaia = getStarWithMinDist(csvGaia, ra, dec, iStar)
    #                print('csvSimbadI: minimum distance = ',dist,': index = ',index,', source_id = ',csvSimbadI.getData('source_id', index),
    #                      ', csvSimbadXGaiaGood: minimum distance good = ',distGood,': index good = ',indexGood,', source_id good = ',csvSimbadXGaiaGood.getData('source_id', indexGood),
    #                     ', minDistGaia = ',minDistGaia,', indexGaia = ',indexGaia,', source_id Gaia = ',csvGaia.getData('source_id',indexGaia),
    #                     )
        if distGood < maxAngularDistance:
            csvOut = csvData.CSVData()
            csvOut.header = csvTemp.header
            csvOut.addColumn('SimbadU')
            csvOut.addColumn('SimbadB')
            csvOut.addColumn('SimbadV')
            csvOut.addColumn('SimbadR')
            csvOut.addColumn('SimbadI')
            row = []
            for key in csvTemp.header:
                row.append(csvGaia.getData(key,indexGood))
            row.append(csvSimbad.getData('SimbadU',iStar))
            row.append(csvSimbad.getData('SimbadB',iStar))
            row.append(csvSimbad.getData('SimbadV',iStar))
            row.append(csvSimbad.getData('SimbadR',iStar))
            row.append(csvSimbad.getData('SimbadI',iStar))
            csvOut.append(row)
            print('adding row <',row,'> to ',outFile)
            moveStarsToXY.appendCSVDataToFile(csvOut,outFile,os.path.join('/var/lock/',outFile[outFile.rfind('/')+1:]))
#            STOP

#process(1000)
if True:#False:
    p = Pool(processes=16)
    iCombo = np.arange(0,len(pixels),1)
    random.shuffle(iCombo)

    p.map(process, iCombo)
    p.close()


#                inFileNameSimbadXGaia = inFileNameSimbadXGaiaRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh)
#                csvSimbadXGaia = csvFree.readCSVFile(inFileNameSimbadXGaia, ',', True)
#                indexSimbadXGaia, minDistSimbadXGaia = getStarWithMinDist(csvSimbadXGaia, ra, dec, iStar)
#                print('csvSimbadI: minimum distance = ',dist,': index = ',index,', source_id = ',csvSimbadI.getData('source_id', index),
#                      '; csvSimbadXGaiaGood: minimum distance good = ',distGood,': index good = ',indexGood,', source_id good = ',csvSimbadXGaiaGood.getData('source_id', indexGood),
#                     '; minDistGaia = ',minDistGaia,', indexGaia = ',indexGaia,', source_id Gaia = ',csvGaia.getData('source_id',indexGaia),
#                     '; minimum distance SimbadXGaia = ',minDistSimbadXGaia,': indexSimbadXGaia = ',indexSimbadXGaia,', source_id SimbadXGaia = ',csvSimbadXGaia.getData('source_id', indexSimbadXGaia))

#                indicesFound = csvGaia.find('source_id',sourceId,0)
#                if indicesFound[0] >= 0:
#                    print('source_id <'+sourceId+'> found in Gaia file at ',indicesFound,': x = ',csvGaia.getData('hammerX', indicesFound[0]),', y = ',csvGaia.getData('hammerY', indicesFound[0]))

#                indicesFound = csvSimbadXGaia.find('source_id',sourceId,0)
#                print('source_id <'+sourceId+'> found in SimbadXGaia file at ',indicesFound)
#                if indicesFound[0] >= 0:
#                    print('source_id <'+sourceId+'> found in SimbadXGaia file at ',indicesFound,': x = ',csvSimbadXGaia.getData('hammerX', indicesFound[0]),', y = ',csvSimbadXGaia.getData('hammerY', indicesFound[0]))

#                indicesFound = csvSimbadXGaiaGood.find('source_id',sourceId,0)
#                print('source_id <'+sourceId+'> found in SimbadXGaiaGood file at ',indicesFound)
#                if indicesFound[0] >= 0:
#                    print('source_id <'+sourceId+'> found in SimbadXGaiaGood file at ',indicesFound,': x = ',csvSimbadXGaiaGood.getData('hammerX', indicesFound[0]),', y = ',csvSimbadXGaiaGood.getData('hammerY', indicesFound[0]))

#                STOP
if False:
    loggsSimbadI = []
    loggsGaia = []
    loggsSimbadXGaia = []
    for pix in pixels:
        inFileNameSimbadI = inFileNameSimbadIRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh)
        try:
            csvSimbadI = csvFree.readCSVFile(inFileNameSimbadI, ',', True)
            if csvSimbadI.size() > 0:
                sourceIdsSimbadI = csvSimbadI.getData('source_id')

                inFileNameGaia = inFileNameGaiaRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh)
                csvGaia = csvFree.readCSVFile(inFileNameGaia, ',', True)

                inFileNameSimbadXGaia = inFileNameSimbadXGaiaRoot % (pix.xLow, pix.xHigh,pix.yLow, pix.yHigh)
                csvSimbadXGaia = csvFree.readCSVFile(inFileNameSimbadXGaia, ',', True)

                for sourceId in sourceIdsSimbadI:
                    indicesFound = csvSimbadI.find('source_id',sourceId,0)
                    loggsSimbadI.append(csvSimbadI.getData('rv_template_logg',indicesFound[0]))
                    print('loggsSimbadI = ',loggsSimbadI)
                    indicesFound = csvGaia.find('source_id',sourceId,0)
                    print('source_id <'+sourceId+'> found in Gaia file at ',indicesFound)
                    if indicesFound[0] >= 0:
                        loggsGaia.append(csvGaia.getData('rv_template_logg',indicesFound[0]))
                        print('logg = <'+loggsGaia[len(loggsGaia)-1]+'>')
                    print('loggsGaia = ',loggsGaia)

                    indicesFound = csvSimbadXGaia.find('source_id',sourceId,0)
                    print('source_id <'+sourceId+'> found in SimbadXGaia file at ',indicesFound)
                    if indicesFound[0] >= 0:
                        loggsSimbadXGaia.append(csvSimbadXGaia.getData('rv_template_logg',indicesFound[0]))
                        print('logg = <'+loggsSimbadXGaia[len(loggsSimbadXGaia)-1]+'>')
                    print('loggsSimbadXGaia = ',loggsSimbadXGaia)
        except Exception as e:
            print('exception <'+str(e)+'> occured')
            pass
