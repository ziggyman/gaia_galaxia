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

from myUtils import hmsToDeg,dmsToDeg,raDecToLonLat,getPixel,angularDistance
#os.system("/Users/azuri/entwicklung/python/myUtils.py")# import getDate, findClosestDate,...

#parameters
maxAngularDistance = 3.0
path = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/'
fnameList = path+'xyfiles.list'
keywordsToFind = []

fnameGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/dr2/xy/GaiaSource_'
fNameXMatchRoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f_R_phot_rp_mean_mag_rv_template_logg.csv'

nStarsDone = 0

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
    for i in range(gaiaData.size()):
#        print('gaiaData.getData(',i,') = ',gaiaData.getData(i))
#        print('gaiaData.getData(parallax,',i,') = ',gaiaData.getData('parallax',i))
        if gaiaData.getData('parallax',i) != '':
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
#            print('c_epoch2000.ra.deg = ',c_epoch2000.ra.deg)
            thisDist = angularDistance(ra, dec, c_epoch2000.ra.deg, c_epoch2000.dec.deg) * 3600.
        else:
            thisDist = angularDistance(ra, dec, float(gaiaData.getData('ra',i)), float(gaiaData.getData('dec',i))) * 3600.
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
print('len(csvSimbad.header) = ',len(csvSimbad.header))
for simbadKeyWord in simbadKeyWords:
    csvSimbad.addColumn(simbadKeyWord)
    print('csvSimbad.header[',len(csvSimbad.header)-1,'] = <'+csvSimbad.header[len(csvSimbad.header)-1]+'>')
print('len(csvSimbad.header) = ',len(csvSimbad.header))

def processSimbadStar(iStar):
#    print('started processSimbadStar: nStarsDone = ',nStarsDone,'processSimbadStar: csvSimbad.size() = ',csvSimbad.size())
    simbadXGaiaFile = '/Volumes/obiwan/azuri/data/simbad/simbad_ImagXGaia.csv'

    ra = float(simbadData.getData('RA', iStar))
    dec = float(simbadData.getData('DEC', iStar))
    lon, lat = raDecToLonLat(ra, dec)
#        print('ra = ',ra,', dec = ',dec,': lon = ',lon,', lat = ',lat)
#        ra, dec = lonLatToRaDec(lon, lat)
#        print('lon = ',lon,', lat = ',lat,': ra = ',ra,', dec = ',dec,)

    xy = ham.lonLatToXY(lon, lat)
    pix = getPixel(xy.x, xy.y)
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
        row = ['' for i in range(len(csvSimbad.header))]
        csvSimbad.append(row)
        print('processSimbadStar: csvSimbad.size() = ',csvSimbad.size())
        if indexXMatch >= 0:
            for gaiaKeyWord in csvGaiaXMatch.header:
                keywordPos = csvSimbad.findKeywordPos(gaiaKeyWord)
                csvSimbad.setData(gaiaKeyWord, csvSimbad.size()-1, csvGaiaXMatch.getData(gaiaKeyWord, indexXMatch))
                print('xMatch found: csvSimbad.data[',csvSimbad.size()-1,', ',gaiaKeyWord,'] = ',csvSimbad.data[csvSimbad.size()-1][keywordPos])
        else:
            for gaiaKeyWord in csvGaia.header:
                keywordPos = csvSimbad.findKeywordPos(gaiaKeyWord)
                csvSimbad.setData(gaiaKeyWord, csvSimbad.size()-1, csvGaia.getData(gaiaKeyWord, index))
                print('xMatch not found: csvSimbad.data[',csvSimbad.size()-1,', ',gaiaKeyWord,'] = ',csvSimbad.data[csvSimbad.size()-1][keywordPos])
        for simbadKeyWord in simbadKeyWords:
            keywordPos = csvSimbad.findKeywordPos(simbadKeyWord)
            csvSimbad.setData(simbadKeyWord, csvSimbad.size()-1, simbadData.getData(simbadKeyWord, iStar))
            print('csvSimbad.data[',csvSimbad.size()-1,', ',simbadKeyWord,'] = ',csvSimbad.data[csvSimbad.size()-1][keywordPos])
        if not os.path.isfile(simbadXGaiaFile):
            csvFree.writeCSVFile(csvSimbad, simbadXGaiaFile)
            print('created <'+simbadXGaiaFile+'>')
        else:
            print('trying to open file <'+simbadXGaiaFile+'>')
            try:
                with open(simbadXGaiaFile,'a') as f:
                    data = csvSimbad.getData(csvSimbad.header[0],csvSimbad.size()-1)
                    print('data = ',data)
                    line = data
                    print('line = <',line,'>')
                    for i in np.arange(1,len(csvSimbad.header)-1):
                        line += ','+csvSimbad.getData(csvSimbad.header[i], csvSimbad.size()-1)
                    line += '\n'
                    print('adding line <'+line+'> to ',simbadXGaiaFile)
                    f.write(line)
            except Exception as e:
                print('exception occured while trying to open file <'+simbadXGaiaFile+'>')
                print(e)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print("*** print_tb:")
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                print("*** print_exception:")
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stdout)
                print("*** print_exc:")
                traceback.print_exc()
                print("*** format_exc, first and last line:")
                formatted_lines = traceback.format_exc().splitlines()
                print(formatted_lines[0])
                print(formatted_lines[-1])
                print("*** format_exception:")
                print(repr(traceback.format_exception(exc_type, exc_value,
                                                      exc_traceback)))
                print("*** extract_tb:")
                print(repr(traceback.extract_tb(exc_traceback)))
                print("*** format_tb:")
                print(repr(traceback.format_tb(exc_traceback)))
                print("*** tb_lineno:", exc_traceback.tb_lineno)
            print('appended line to <'+simbadXGaiaFile+'>')
#    nStarsDone += 1
#    print(nStarsDone,' stars finished')


if not os.path.isfile(simbadXGaiaFile):
#    x = [float(a) for a in simbadData.getData('RA')]
#    y = [float(a) for a in simbadData.getData('DEC')]
#    print('x = ',len(x),': ',x)
#    print('y = ',len(y),': ',y)
#    plt.scatter(x = np.array(x), y = np.array(y), s=0.3)
#    plt.savefig('/Users/azuri/entwicklung/gaia_galaxia/RA-DEC.pdf', format='pdf', frameon=False, bbox_inches='tight', pad_inches=0.1)
#    plt.show()
    simbadStars = [i for i in range(simbadData.size())]
#    print('simbadStars = ',type(simbadStars),': ',simbadStars)
    random.shuffle(simbadStars)
    p = Pool(processes=16)
#    processSimbadStar(simbadStars)
    p.map(processSimbadStar, simbadStars)
    p.close()
#    csvSimbad = findSimbadStarsInGaia(simbadData)
#    csvFree.writeCSVFile(csvSimbad, simbadXGaiaFile)
STOP

def crossMatch(simbadFile, gaiaFile):
    simbadData = csvFree.readCSVFile(simbadFile)
    print('simbadData.header = ',simbadData.header)
    gaiaData = csvFree.readCSVFile(gaiaFile)
    print('gaiaData.header = ',gaiaData.header)

    outData = csvFree.crossMatch(simbadData, gaiaData, 'source_id')
    print('crossMatch: found ',outData.size(),' matching stars out of ',simbadData.size(),' stars in Simbad catalogue and ',gaiaData.size(),' stars in GAIA catalogue')
    return outData

# data: dictionary
def getGoodStarIndices(data, keywords):
    goodStars = []

    cols = []
    for keyword in keywords[0]:
        cols.append(data.getData(keyword))
    for keyword in keywords[1:]:
        cols.append(data.getData(keyword))
#    b = data.getData('B')
#    print('b = ',b)
#    v = data.getData('V')
#    print('v = ',v)
#    r = data.getData('R')
#    print('r = ',r)
#    g_bp = data.getData('phot_bp_mean_mag')
#    print('g_bp = ',g_bp)
#    dist = data.getData('angDist')
#    print('dist = ',dist)
#    logg = data.getData('rv_template_logg')
#    print('logg = ',logg)

    for i in range(data.size()):
        isGood = True
        for col in cols:
            if col[i] == '':
                isGood = False
        if isGood:
            goodStars.append(i)
    return goodStars

def getPixel(fName):
    pixel = fName[fName.rfind('d_')+2:fName.rfind('.csv')]
    return pixel

def process(fileNumber):
    fname = path+fnames[fileNumber]
    print('reading file <'+fname+'>')
    #dat = csvFree.readCSVFile(fname)
    fnameGaia = fnameGaiaRoot+getPixel(fname)+'.csv'

    keywordsToFind = [[['B','V','R'],'phot_bp_mean_mag','rv_template_logg'],
                      #['u','g','r','phot_bp_mean_mag','rv_template_logg'],
                      #['r','i','z','phot_rp_mean_mag','rv_template_logg'],
                      [['R'],'phot_rp_mean_mag','rv_template_logg'],
                      ]
#    fnameOut = fname[0:fname.rfind('.')]
#    for key in keywordsToFind[3]:
#        fnameOut += '_'+key
#    fnameOut += '.csv'
#    print('searching for file <'+fnameOut+'>')
    if True:# not os.path.isfile(fnameOut):
        #print('file <'+fnameOut+'> not found: calculating')

        csvData = csvFree.readCSVFile(fname)
        dat = crossMatch(fname, fnameGaia)
        #print('dat.header = ',dat.header)
        #print dat.getData('phot_bp_mean_mag')[0:]

        """get indices of stars which have data for B, V, R, and G_BP"""
        print('searching for stars with all needed parameters')
        for keys in keywordsToFind:
            csvData.header = dat.header
            goodStars = getGoodStarIndices(dat, keys)
            print('found ',len(goodStars),' good stars')
            csvData.data = dat.getData(goodStars)
            if (keys[0][0] == 'B') or (keys[0][0] == 'R'):
                for key in simbadKeyWords:
                    csvData.header.append(key)
                    for i in range(csvData.size()):
                        csvData.data[i].append('')
                for i in range(csvSimbad.size()):
                    isGood = True
                    for key in keys[0]:
                        if csvSimbad.getData('Simbad'+key, i) == '':
                            isGood = False
                    idx = csvData.find(csvSimbad.getData('source_id', i))
                    if idx >= 0:
                        for key in simbadKeyWords:
                            csvData.data[idx][csvData.findKeywordPos(key)] = csvSimbad.getData(key, i)
                    else:
                        if isGood:
                            newRow = []
                            for col in range(len(csvData.header)):
                                newRow.append('')
                            csvData.append(newRow)
                            for key in csvSimbad.header:
                                csvData.data[csvData.size()-1][csvData.findKeywordPos(key)] = csvSimbad.getData(key,i)
            fnameOut = fname[0:fname.rfind('.')]
            for key in keys[0]:
                fnameOut += '_'+key
            if keys[0][0] == 'R':
                fnameOut += '_I'
            for key in keys[1:]:
                fnameOut += '_'+key
            fnameOut += '.csv'
            print('writing file <'+fnameOut+'>')
            csvFree.writeCSVFile(csvData, fnameOut)

if True:
    """cross-match (Simbad x Gaia) with GAIA DR2"""
    with open(fnameList) as f:
        fnames = f.read().splitlines()

    p = Pool(processes=16)
    iCombo = range(len(fnames))
    random.shuffle(iCombo)

    p.map(process, iCombo)
    p.close()
