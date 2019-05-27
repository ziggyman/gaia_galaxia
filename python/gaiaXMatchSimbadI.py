#!/usr/bin/env python
from multiprocessing import Pool
import os
import random

import astropy.units as u
from astropy.coordinates import SkyCoord, Distance
from astropy.time import Time
import matplotlib.pyplot as plt
import numpy as np
import sys, traceback

#import csv
import csvData
import csvFree
import hammer
import moveStarsToXY

from myUtils import hmsToDeg,dmsToDeg,raDecToLonLat,getPixel,angularDistance
#os.system("/Users/azuri/entwicklung/python/myUtils.py")# import getDate, findClosestDate,...

#TODO: check maximum distance in outfiles

doSimbadI = False#True

maxAngularDistance = 5.0

#parameters
path = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/'
fnameList = path+'xyfiles.list'

fnameGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/dr2/xy/GaiaSource_'
fNameXMatchRoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f.csv'

nStarsDone = 0

def getPixelI(pixel, pixels):
    for i in np.arange(0,len(pixels),1):
        if (pixel.xLow == pixels[i].xLow) and (pixel.xHigh == pixels[i].xHigh) and (pixel.yLow == pixels[i].yLow) and (pixel.yHigh == pixels[i].yHigh):
            return i
    return -1

def readImags(fname):
    data = csvData.CSVData()
    data.header = ['RA','DEC','SimbadU','SimbadB','SimbadV','SimbadR','SimbadI']
    with open(fname,'r') as f:
        for line in f:
            lst = []
            lineStr = line.strip('\n')
            cols = lineStr.split('|')
            if len(cols) > 4:
                if (cols[0].replace(' ','') != '#') and cols[0][0] != '-':
                    RA = cols[3].strip(' ')
                    RA = RA[0:RA.rfind(' ')]
                    RA = RA[0:RA.rfind(' ')]
                    RA = RA[0:RA.rfind(' ')]
                    RA = RA.strip(' ')
                    RA = RA.replace(' ',':')
                    lst.append(str(hmsToDeg(RA)))

                    DEC = cols[3][cols[3].find(' ')+1:]
                    DEC = DEC[DEC.find(' ')+1:]
                    DEC = DEC[DEC.find(' ')+1:]
                    DEC = DEC.strip(' ')
                    DEC = DEC.replace(' ',':')
                    lst.append(str(dmsToDeg(DEC)))

                    lst.append(str(cols[4].replace(' ','').replace('~','')))
                    lst.append(str(cols[5].replace(' ','').replace('~','')))
                    lst.append(str(cols[6].replace(' ','').replace('~','')))
                    lst.append(str(cols[7].replace(' ','').replace('~','')))
                    lst.append(str(cols[8].replace(' ','').replace('~','')))
                    data.append(lst)
    print('data.size() = ',data.size())
    return data

def getStarWithMinDist(gaiaData, ra, dec, iStar=0):
    dist = None
    index = None
    print('gaiaData.header = ',gaiaData.header)
    for i in np.arange(0,gaiaData.size(),1):
#        print('gaiaData.getData(',i,') = ',gaiaData.getData(i))
#        print('gaiaData.getData(parallax,',i,') = ',gaiaData.getData('parallax',i))
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
            c = SkyCoord(ra=float(gaiaData.getData('ra',i))*u.degree,
                         dec=float(gaiaData.getData('dec',i))*u.degree,
                         distance=distance,
                         pm_ra_cosdec=float(gaiaData.getData('pmra',i)) * u.mas/u.yr,
                         pm_dec=float(gaiaData.getData('pmdec',i)) * u.mas/u.yr,
                         obstime=time)
#            print('c = ',c)
            c_epoch2000 = c.apply_space_motion(Time('2000-01-01'))
#            print('c_epoch2000 = ',c_epoch2000)
#            print('c_epoch2000 = ',type(c_epoch2000),': ',dir(c_epoch2000),': ',c_epoch2000)
#            print('c_epoch2000.ra = ',type(c_epoch2000.ra),': ',dir(c_epoch2000.ra),': ',c_epoch2000.ra)
            #print('c_epoch2000.ra.deg = ',c_epoch2000.ra.deg)
            thisDist = angularDistance(ra*u.degree, dec*u.degree, c_epoch2000.ra.deg*u.degree, c_epoch2000.dec.deg*u.degree) * 3600.
        else:
            thisDist = angularDistance(ra*u.degree, dec*u.degree, float(gaiaData.getData('ra',i))*u.degree, float(gaiaData.getData('dec',i))*u.degree) * 3600.
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

simbadXGaiaFile = '/Volumes/obiwan/azuri/data/simbad/simbad_ImagXGaia.csv'
simbadData = readImags('/Volumes/obiwan/azuri/data/simbad/simbad_Imag_20000stars.txt')
print('simbadData.header = ',simbadData.header)
#def findSimbadStarsInGaia(simbadData):
simbadKeyWords = ['SimbadU','SimbadB','SimbadV','SimbadR','SimbadI']
ham = hammer.Hammer()
pixels = ham.getPixels()
fnameGaia = fNameXMatchRoot % (pixels[0].xLow, pixels[0].xHigh, pixels[0].yLow, pixels[0].yHigh)
print('fnameGaia = <'+fnameGaia+'>')
csvGaia = csvFree.readCSVFile(fnameGaia)
csvSimbad = csvData.CSVData()
csvSimbad.header = csvGaia.header
print('csvGaia.header = ',len(csvGaia.header),': ',csvGaia.header)
print('csvSimbad.header = ',len(csvSimbad.header),': ',csvSimbad.header)
for simbadKeyWord in simbadKeyWords:
    csvSimbad.addColumn(simbadKeyWord)
    print('csvSimbad.header[',len(csvSimbad.header)-1,'] = <'+csvSimbad.header[len(csvSimbad.header)-1]+'>')
print('len(csvSimbad.header) = ',len(csvSimbad.header))
if doSimbadI:
    moveStarsToXY.writeHeaderToOutFiles(csvSimbad.header,
                               pixels,
                               "gaiaXSimbadI",
                               False,
                               '/Volumes/obiwan/azuri/data/simbad/xy/')

def processSimbadStar(iStar):
#    print('started processSimbadStar: nStarsDone = ',nStarsDone,'processSimbadStar: csvSimbad.size() = ',csvSimbad.size())
    simbadXGaiaFile = '/Volumes/obiwan/azuri/data/simbad/simbad_ImagXGaia.csv'

    csvOut = csvData.CSVData()
    csvOut.header = csvSimbad.header
#    print(iStar,' = iStar')
    ra = float(simbadData.getData('RA', iStar))
    dec = float(simbadData.getData('DEC', iStar))
    lon, lat = raDecToLonLat(ra, dec)
#        print('ra = ',ra,', dec = ',dec,': lon = ',lon,', lat = ',lat)
#        ra, dec = lonLatToRaDec(lon, lat)
#        print('lon = ',lon,', lat = ',lat,': ra = ',ra,', dec = ',dec,)

    xy = ham.lonLatToXY(lon, lat)
    pix = getPixel(xy.x, xy.y)
    print('iStar = ',iStar,': lon = ',lon,', lat = ',lat,': x = ',xy.x,', y = ',xy.y,': pix = ',pix)
    iPix = getPixelI(pix,pixels)
    fnameGaia = fnameGaiaRoot+'%.6f-%.6f_%.6f-%.6f.csv' % (pix.xLow, pix.xHigh, pix.yLow, pix.yHigh)
#        print('fnameGaia = <'+fnameGaia+'>')
    csvGaia = csvFree.readCSVFile(fnameGaia)
#        print('read ',csvGaia.size(),' stars from')
    index, dist = getStarWithMinDist(csvGaia, ra, dec, iStar)
    print('minimum distance = ',dist,': index = ',index)
    if dist < maxAngularDistance:
        #search for star in gaia X simbad file
        fnameGaia = fNameXMatchRoot % (pix.xLow, pix.xHigh, pix.yLow, pix.yHigh)
        csvGaiaXMatch = csvFree.readCSVFile(fnameGaia)
        indexXMatch = csvGaiaXMatch.find('source_id', csvGaia.getData('source_id', index))
        row = ['' for i in np.arange(0,len(csvSimbad.header),1)]
        csvSimbad.append(row)
        print('processSimbadStar: csvSimbad.size() = ',csvSimbad.size())
        if len(indexXMatch) > 1:
            print('len(indexXMatch=',indexXMatch,') = ',len(indexXMatch))
            STOP
        if indexXMatch[0] >= 0:
            for gaiaKeyWord in csvGaiaXMatch.header:
                keywordPos = csvSimbad.findKeywordPos(gaiaKeyWord)
                csvSimbad.setData(gaiaKeyWord, csvSimbad.size()-1, csvGaiaXMatch.getData(gaiaKeyWord, indexXMatch[0]))
                print('xMatch found: csvSimbad.data[',csvSimbad.size()-1,', ',gaiaKeyWord,'] = ',csvSimbad.data[csvSimbad.size()-1][keywordPos])
        #else:
        for gaiaKeyWord in csvGaia.header:
            keywordPos = csvSimbad.findKeywordPos(gaiaKeyWord)
            csvSimbad.setData(gaiaKeyWord, csvSimbad.size()-1, csvGaia.getData(gaiaKeyWord, index))
            print('xMatch not found: csvSimbad.data[',csvSimbad.size()-1,', ',gaiaKeyWord,'] = ',csvSimbad.data[csvSimbad.size()-1][keywordPos])
        for simbadKeyWord in simbadKeyWords:
            keywordPos = csvSimbad.findKeywordPos(simbadKeyWord)
            csvSimbad.setData(simbadKeyWord, csvSimbad.size()-1, simbadData.getData(simbadKeyWord, iStar))
            print('csvSimbad.data[',csvSimbad.size()-1,', ',simbadKeyWord,'] = ',csvSimbad.data[csvSimbad.size()-1][keywordPos])
        data = csvSimbad.getData(csvSimbad.size()-1)
        print('len(data) = ',len(data))
        csvOut.append(data)
        nStarsWritten = moveStarsToXY.appendCSVDataToXYFiles(csvOut,
                            pixels,
                            "gaiaXSimbadI",
                            ['source_id'],
                            False,
                            "sim",
                            '/Volumes/obiwan/azuri/data/simbad/xy/')
        print(nStarsWritten,' written to gaiaXSimbad XY file')
        if not os.path.isfile(simbadXGaiaFile):
            csvFree.writeCSVFile(csvSimbad, simbadXGaiaFile)
            print('created <'+simbadXGaiaFile+'>')
        else:
            csvTemp = csvData.CSVData()
            csvTemp.header = csvSimbad.header
            csvTemp.append(csvSimbad.getData(csvSimbad.size()-1))
            moveStarsToXY.appendCSVDataToFile(csvTemp,
                                simbadXGaiaFile,
                                "/var/lock/gaiaXSimbadI.lock")
        print('appended line to <'+simbadXGaiaFile+'>')
#    nStarsDone += 1
#    print(nStarsDone,' stars finished')

if doSimbadI:
    if not os.path.isfile(simbadXGaiaFile):
    #    x = [float(a) for a in simbadData.getData('RA')]
    #    y = [float(a) for a in simbadData.getData('DEC')]
    #    print('x = ',len(x),': ',x)
    #    print('y = ',len(y),': ',y)
    #    plt.scatter(x = np.array(x), y = np.array(y), s=0.3)
    #    plt.savefig('/Users/azuri/entwicklung/gaia_galaxia/RA-DEC.pdf', format='pdf', frameon=False, bbox_inches='tight', pad_inches=0.1)
    #    plt.show()

        simbadStars = [i for i in np.arange(0,simbadData.size(),1)]

    #    for simbadStar in simbadStars[100:]:
     #       processSimbadStar(simbadStar)
     #   STOP
    #    print('simbadStars = ',type(simbadStars),': ',simbadStars)
    #    random.shuffle(simbadStars)
        p = Pool(processes=16)
    #    processSimbadStar(simbadStars)
        p.map(processSimbadStar, simbadStars)
        p.close()
    #    csvSimbad = findSimbadStarsInGaia(simbadData)
    #    csvFree.writeCSVFile(csvSimbad, simbadXGaiaFile)
    STOP
