#!/usr/bin/env python
import csv
import csvData
import csvFree
from multiprocessing import Pool
import os
import random

#parameters
path = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/'
fnameList = path+'xyfiles.list'

fnameGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/dr2/xy/GaiaSource_'

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
    for keyword in keywords:
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

    keywordsToFind = [['B','V','R','phot_bp_mean_mag','rv_template_logg'],
                      ['u','g','r','phot_bp_mean_mag','rv_template_logg'],
                      ['i','z','phot_rp_mean_mag','rv_template_logg'],
                      ['R','phot_rp_mean_mag','rv_template_logg'],
                      ]
    fnameOut = fname[0:fname.rfind('.')]
    for key in keywordsToFind[3]:
        fnameOut += '_'+key
    fnameOut += '.csv'
    print('searching for file <'+fnameOut+'>')
    if not os.path.isfile(fnameOut):
        print('file <'+fnameOut+'> not found: calculating')

        csvData = csvFree.readCSVFile(fname)
        dat = crossMatch(fname, fnameGaia)
        #print('dat.header = ',dat.header)
        #print dat.getData('phot_bp_mean_mag')[0:]

        """get indices of stars which have data for B, V, R, and G_BP"""
        print('searching for stars with all needed parameters')
        for keys in keywordsToFind:
            csvData.header = dat.header
            goodStars = getGoodStarIndices(dat, keys)
            print 'found ',len(goodStars),' good stars'
            csvData.data = dat.getData(goodStars)
            fnameOut = fname[0:fname.rfind('.')]
            for key in keys:
                fnameOut += '_'+key
            fnameOut += '.csv'
            print('writing file <'+fnameOut+'>')
            csvFree.writeCSVFile(csvData, fnameOut)


"""cross-match (Simbad x Gaia) with GAIA DR2"""
with open(fnameList) as f:
    fnames = f.read().splitlines()

p = Pool(processes=16)
iCombo = range(len(fnames))
random.shuffle(iCombo)

p.map(process, iCombo)
p.close()
