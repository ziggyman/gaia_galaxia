#!/usr/bin/env python
from multiprocessing import Pool
import os
import random
import numpy as np

#import csv
import csvData
import csvFree
import hammer

#parameters
path = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/'
fnameList = path+'xyfiles.list'

fnameGaiaRoot = '/Volumes/obiwan/azuri/data/gaia/dr2/xy/GaiaSource_'
fNameXMatchRoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f.csv'

nStarsDone = 0

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

def getPixelFromFileName(fName):
    pixel = fName[fName.rfind('d_')+2:fName.rfind('.csv')]
    return pixel

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

    for i in np.arange(0,data.size(),1):
        isGood = True
        for col in cols:
            if col[i] == '':
                isGood = False
        if isGood:
            goodStars.append(i)
    return goodStars

def process(fileNumber):
    fname = path+fnames[fileNumber]
    print('reading file <'+fname+'>')
    #dat = csvFree.readCSVFile(fname)
    fnameGaia = fnameGaiaRoot+getPixelFromFileName(fname)+'.csv'

    keywordsToFind = [#[['B','V','R'],'phot_g_mean_mag','rv_template_logg'],
                      #[['B','V'],'phot_bp_mean_mag','rv_template_logg'],
                      #[['u','g','r'],'phot_bp_mean_mag','rv_template_logg'],
                      #[['g','r'],'phot_bp_mean_mag','rv_template_logg'],
                      [['g','r','i','z'],'phot_g_mean_mag','rv_template_logg'],
                      #[['r','i','z'],'phot_rp_mean_mag','rv_template_logg'],
                      #[['R'],'phot_rp_mean_mag','rv_template_logg'],
                      ]
    if True:# not os.path.isfile(fnameOut):
        #print('file <'+fnameOut+'> not found: calculating')

        csvData = csvFree.readCSVFile(fname)
        if csvData.size() > 0:
            dat = crossMatch(fname, fnameGaia)
            #print('dat.header = ',dat.header)
            #print dat.getData('phot_bp_mean_mag')[0:]
            fnameOut = os.path.join(fname[0:fname.rfind('/')+1]+'temp', fname[fname.rfind('/')+1:fname.rfind('.')])

            csvFree.writeCSVFile(csvData, fnameOut+'.csv')

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
                        for i in np.arange(0,csvData.size(),1):
                            csvData.data[i].append('')
                    for i in np.arange(0,csvSimbad.size(),1):
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
                                for col in np.arange(0,len(csvData.header),1):
                                    newRow.append('')
                                csvData.append(newRow)
                                for key in csvSimbad.header:
                                    csvData.data[csvData.size()-1][csvData.findKeywordPos(key)] = csvSimbad.getData(key,i)
                fnameOut = os.path.join(fname[0:fname.rfind('/')+1]+'temp', fname[fname.rfind('/')+1:fname.rfind('.')])
                print('fnameOut = <'+fnameOut+'>')
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
    iCombo = np.arange(0,len(fnames),1)
    print('iCombo = ',iCombo)
#    for iFile in iCombo:
#        process(iFile)
#    random.shuffle(iCombo)

    p.map(process, iCombo)
    p.close()
