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

#parameters
pathOut = ''
fNameARoot = ''
fNameBRoot = ''
fNameOutRoot = ''

#filterSet = "JohnsonCousins"#,
filterSet = "ugriz"

if filterSet == 'ugriz':
    pathOut = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2+Simbad+SDSS/xy/'
    fNameARoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/temp/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f_%s.csv'
    fNameBRoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/xy/Gaia+SDSS_%.6f-%.6f_%.6f-%.6f.csv'
    fnameOutRoot = os.path.join(pathOut,'GaiaXSimbad+SDSS_%.6f-%.6f_%.6f-%.6f_%s.csv')
    keywordsToFindA = [[['g','r','i','z'],'phot_g_mean_mag','rv_template_logg'],
                        #[['g','r'],'phot_bp_mean_mag','rv_template_logg'],
                        #[['r','i','z'],'phot_rp_mean_mag','rv_template_logg'],
                       ]
    keywordsToFindB = [[['gmag','rmag','imag','zmag'],'phot_g_mean_mag','rv_template_logg'],
                          #[['gmag','rmag'],'phot_bp_mean_mag','rv_template_logg'],
                          #[['rmag','imag','zmag'],'phot_rp_mean_mag','rv_template_logg'],
                         ]
else:
    pathOut = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2XSimbadXSimbadI/xy'
    fNameARoot = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/xy/GaiaXSimbad_%.6f-%.6f_%.6f-%.6f_%s.csv'
    fNameBRoot = '/Volumes/obiwan/azuri/data/simbad/xy/GaiaXSimbadI_%.6f-%.6f_%.6f-%.6f.csv'
    fnameOutRoot = os.path.join(pathOut,'GaiaXSimbadXSimbadI_%.6f-%.6f_%.6f-%.6f_%s.csv')

    keywordsToFindA = [[['B','V','R','I'],'phot_g_mean_mag','rv_template_logg'],
                        [['B','V'],'phot_bp_mean_mag','rv_template_logg'],
                        [['B','V','R'],'phot_bp_mean_mag','rv_template_logg'],
                        [['R','I'],'phot_rp_mean_mag','rv_template_logg'],
                      ]
    keywordsToFindB = [[['SimbadB','SimbadV','SimbadR','SimbadI'],'phot_g_mean_mag','rv_template_logg'],
                        [['SimbadB','SimbadV'],'phot_bp_mean_mag','rv_template_logg'],
                        [['SimbadB','SimbadV','SimbadR'],'phot_bp_mean_mag','rv_template_logg'],
                        [['SimbadR','SimbadI'],'phot_rp_mean_mag','rv_template_logg'],
                      ]
#fnameList = path+'xyfiles.list'


nStarsDone = 0
ham = hammer.Hammer()
pixels = ham.getPixels()

idKeyword = 'source_id'

# data: dictionary
def getGoodStarIndices(data, keywords):
#    print('getGoodStarIndices: data.header = ',data.header)
#    print('getGoodStarIndices: keywords = <',keywords,'>')
    goodStars = []

    cols = []
    for keyword in keywords[0]:
#        print('getGoodStarIndices: keyword = <',keyword,'>')
        if keyword != 'I':
            cols.append(data.getData(keyword))
    for keyword in keywords[1:]:
#        print('getGoodStarIndices: keyword = <',keyword,'>')
        cols.append(data.getData(keyword))

    for i in np.arange(0,data.size(),1):
        isGood = True
        for col in cols:
            if col[i] == '':
                isGood = False
        if isGood:
            goodStars.append(i)
    return goodStars

def getGoodStarIndicesFromBoth(dataA, idKeywordA, keywordsA, dataB, idKeywordB, keywordsB):
    print('getGoodStarIndicesBoth: dataA.header = ',dataA.header)
    print('getGoodStarIndicesBoth: dataB.header = ',dataB.header)
    print('getGoodStarIndicesBoth: keywordsA = <',keywordsA,'>')
    print('getGoodStarIndicesBoth: keywordsB = <',keywordsB,'>')
    goodStars = []

    for iStarA in np.arange(0,dataA.size(),1):
        isGood = True
        idStar = dataA.getData(idKeywordA, iStarA)
        print('searching for star with id '+idStar+' in dataset B')
        iStarB = dataB.find(idKeywordB, idStar, 0)[0]
        if iStarB >= 0:
            print('star with id '+idStar+' found in dataset B')
            for iKey in np.arange(0,len(keywordsA[0]),1):
                a = keywordsA[0][iKey]
                b = keywordsB[0][iKey]
                print('keywordA = <'+a+'>, keywordB = <'+b+'>')
                if a != 'I':
                    if (dataA.getData(a,iStarA) == '') and (dataB.getData(b,iStarB) == ''):
                        isGood = False
                else:
                    if dataB.getData(b,iStarB) == '':
                        isGood = False
            for iKey in np.arange(1,len(keywordsA),1):
                a = keywordsA[iKey]
                b = keywordsB[iKey]
                if (dataA.getData(a,iStarA) == '') and (dataB.getData(b,iStarB) == ''):
                    isGood = False
        if isGood:
            print('star with id '+idStar+' is good')
            goodStars.append([iStarA,iStarB])
    return goodStars

def getPixel(fName):
    pixel = fName[fName.rfind('d_')+2:fName.rfind('.csv')]
    return pixel

def process(iPix):

    if True:# not os.path.isfile(fnameOut):

        """get indices of stars which have data for all required keys"""
#        print('searching for stars with all needed parameters')
        for iKeys in np.arange(0,len(keywordsToFindA),1):
            print('iKeys = ',iKeys)
            keysSimbad = keywordsToFindA[iKeys]
            keysSDSS = keywordsToFindB[iKeys]

            keyStr = keysSimbad[0][0]
            for key in keysSimbad[0][1:]:
                if keyStr != 'I':
                    keyStr += '_'+key
            for key in keysSDSS[0]:
                keyStr += '_'+key
            for key in keysSimbad[1:]:
                keyStr += '_'+key
            print('keyStr = <'+keyStr+'>')

            fnameOut = fnameOutRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh, keyStr)

            if not os.path.isfile(fnameOut):
                print('file <'+fnameOut+'> not found')
                keyStrSimbad = keysSimbad[0][0]
                for key in keysSimbad[0][1:]:
                    if key != 'I':
                        keyStrSimbad += '_'+key
                for key in keysSimbad[1:]:
                    keyStrSimbad += '_'+key
                fNameGaiaXSimbad = fNameARoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh, keyStrSimbad)
                print('fNameGaiaXSimbad = <'+fNameGaiaXSimbad+'>')
                if os.path.isfile(fNameGaiaXSimbad):
                    csvGaiaXSimbad = csvFree.readCSVFile(fNameGaiaXSimbad,',',True)
                    print('csvGaiaXSimbad.header = ',len(csvGaiaXSimbad.header),': ',csvGaiaXSimbad.header)
                    print(' ')

                    fNameGaiaXSDSS = fNameBRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh)
                    print('fNameGaiaXSDSS = <'+fNameGaiaXSDSS+'>')
                    if os.path.isfile(fNameGaiaXSDSS):
                        csvGaiaXSDSS = csvFree.readCSVFile(fNameGaiaXSDSS,',',True)
                        print('csvGaiaXSDSS.header = ',len(csvGaiaXSDSS.header),': ',csvGaiaXSDSS.header)
                        print(' ')

                        csvDataOut = csvData.CSVData()
                        for key in csvGaiaXSimbad.header:
                            csvDataOut.addColumn(key)
                            print('added key=<'+key+'> from csvGaiaXSimbad.header to csvDataOut.header => len=',len(csvDataOut.header))
                        for key in csvGaiaXSDSS.header:
                            if key not in csvDataOut.header:
                                csvDataOut.addColumn(key)
                                print('added key=<'+key+'> from csvGaiaXSDSS.header to csvDataOut.header => len=',len(csvDataOut.header))
                            else:
                                print('key=<'+key+'> from csvGaiaXSDSS.header already in csvDataOut.header => len=',len(csvDataOut.header))
                        print('csvDataOut.header = ',len(csvDataOut.header),': ',csvDataOut.header)
                        print(' ')

                        for goodRun in [0,1]:
                            goodStarsGaiaXSimbad = []
                            goodStarsGaiaXSDSS = []
                            goodStarsBoth = []
                            if goodRun == 0:
                                goodStarsGaiaXSimbad = getGoodStarIndices(csvGaiaXSimbad, keywordsToFindA[iKeys])
                                goodStarsGaiaXSDSS = getGoodStarIndices(csvGaiaXSDSS, keywordsToFindB[iKeys])
                            else:
                                if csvGaiaXSDSS.size() > 0:
                                    print('keywordsToFindA = ',keywordsToFindA)
                                    print('keywordsToFindA[',iKeys,'] = ',keywordsToFindA[iKeys])
                                    print('keywordsToFindB = ',keywordsToFindB)
                                    print('keywordsToFindB[',iKeys,'] = ',keywordsToFindB[iKeys])
                                    goodStarsBoth = getGoodStarIndicesFromBoth(csvGaiaXSimbad,
                                                                               idKeyword,
                                                                               keywordsToFindA[iKeys],
                                                                               csvGaiaXSDSS,
                                                                               idKeyword,
                                                                               keywordsToFindB[iKeys])
                                    goodStarsGaiaXSimbad = [xx[0] for xx in goodStarsBoth]
                                    goodStarsGaiaXSDSS = [xx[1] for xx in goodStarsBoth]

                            print('found ',len(goodStarsGaiaXSimbad),' good stars out of ',csvGaiaXSimbad.size(),' stars')
                            print('goodStarsGaiaXSimbad = ',goodStarsGaiaXSimbad)

                            print('len(goodStarsGaiaXSDSS) = ',len(goodStarsGaiaXSDSS))

                            rowsOut = []
                            if (len(goodStarsGaiaXSimbad) > 0) and (goodStarsGaiaXSimbad[0] >= 0):
                                rowsOut = csvGaiaXSimbad.getData(goodStarsGaiaXSimbad)
                                print('len(goodStarsGaiaXSimbad) > 0: len(rowsOut) = ',len(rowsOut),', len(rowsOut[0]) = ',len(rowsOut[0]))
                                for iKey in np.arange(len(csvGaiaXSimbad.header), len(csvDataOut.header),1):
        #                            print('iKey = ',iKey)
                                    for iRowOut in np.arange(0,len(rowsOut),1):
                                        rowsOut[iRowOut].append('')
        #                                print('len(rowsOut[',iRowOut,']) = ',len(rowsOut[iRowOut]))
                            print('rowsOut = ',len(rowsOut))
                            if len(rowsOut) > 0:
                                print('len(rowsOut[0]) = ',len(rowsOut[0]))
                                if len(rowsOut[0]) != len(csvDataOut.header):
                                    print('ERROR: len(rowsOut[0])=',len(rowsOut[0]),' != len(csvDataOut.header)=',len(csvDataOut.header))
                            isBad = False
                            for iRrow in np.arange(0,len(rowsOut),1):
                                if len(rowsOut[iRrow]) != len(csvDataOut.header):
                                    print('ERROR: len(rowsOut[',iRrow,'])=',len(rowsOut[iRrow]),' != len(csvDataOut.header)=',len(csvDataOut.header))
                                    isBad = True
                            if isBad:
                                STOP
                            if len(rowsOut) > 0:
                                if goodRun == 0:
                                    csvDataOut.data = rowsOut
                                else:
                                    for iSimbad in np.arange(0,len(goodStarsGaiaXSimbad),1):
                                        posInOut = csvDataOut.find('source_id',csvGaiaXSimbad.getData('source_id',goodStarsGaiaXSimbad[iSimbad]), 0)
                                        if posInOut[0] < 0:
                                            csvDataOut.append(rowsOut[iSimbad])

                #            print('csvGaiaXSimbad.getData(0)[0] = ',csvGaiaXSimbad.getData(0)[0])
                #            print('csvGaiaXSimbad.getData(',csvGaiaXSimbad.header[0],',0) = ',csvGaiaXSimbad.getData(csvGaiaXSimbad.header[0],0))
                #            STOP
                            print('goodStarsGaiaXSDSS = ',len(goodStarsGaiaXSDSS),': ',goodStarsGaiaXSDSS)
                            if (len(goodStarsGaiaXSDSS) > 0) and (goodStarsGaiaXSDSS[0] >= 0):
                                print('goodStarsGaiaXSDSS[0] = ',goodStarsGaiaXSDSS[0])
                                for iStar in np.arange(0,len(goodStarsGaiaXSDSS),1):
                                    if goodStarsGaiaXSDSS[iStar] >= 0:
                                        print('iStar = ',iStar)
                                        print('goodStarsGaiaXSDSS[iStar] = ',goodStarsGaiaXSDSS[iStar])
                                        print("csvGaiaXSDSS.getData('source_id',goodStarsGaiaXSDSS[iStar]) = ",csvGaiaXSDSS.getData('source_id',goodStarsGaiaXSDSS[iStar]))
                                        posFoundInCsvOut = csvDataOut.find('source_id',csvGaiaXSDSS.getData('source_id',goodStarsGaiaXSDSS[iStar]), 0)
                                        print('posFoundInCsvOut = ',posFoundInCsvOut)
                                        if posFoundInCsvOut[0] < 0:# star iStar NOT found in csvDataOut
                                            rowOut = []
                                            print('star ',iStar,' with source_id=<'+csvGaiaXSDSS.getData('source_id',goodStarsGaiaXSDSS[iStar])+'> from GaiaXSDSS NOT found in GaiaXSimbad')
                                            print('csvDataOut.header = ',len(csvDataOut.header),': ',csvDataOut.header)
                                            for key in csvDataOut.header:
                                                if key in csvGaiaXSDSS.header:
                                                    rowOut.append(csvGaiaXSDSS.getData(key,goodStarsGaiaXSDSS[iStar]))
                                                else:
                                                    rowOut.append('')
                                            print('not found: rowOut = ',len(rowOut),': ',rowOut)
                                            if len(rowOut) != len(csvDataOut.header):
                                                print('ERROR: len(rowOut)=',len(rowOut),' != len(csvDataOut.header)=',len(csvDataOut.header))
                                                STOP
                                            csvDataOut.append(rowOut)
                                            print('not found: csvDataOut = ',csvDataOut.size(),': last row = ',csvDataOut.data[csvDataOut.size()-1])
                                        else: # star iStar WAS found in csvDataOut
                                            print('star ',iStar,' with source_id=<'+csvGaiaXSDSS.getData('source_id',goodStarsGaiaXSDSS[iStar])+'> from GaiaXSDSS found in csvDataOut (GaiaXSimbad)')
                                            print('csvGaiaXSDSS.header = ',len(csvGaiaXSDSS.header),': ',csvGaiaXSDSS.header)
                                            print(' ')
                                            print('csvGaiaXSimbad.header = ',len(csvGaiaXSimbad.header),': ',csvGaiaXSimbad.header)
                                            print(' ')
                                            print('csvDataOut.header = ',len(csvDataOut.header),': ',csvDataOut.header)
                                            print(' ')
                                            print('csvDataOut.header[len(csvGaiaXSimbad.header):] = ',len(csvDataOut.header[len(csvGaiaXSimbad.header):]),': ',csvDataOut.header[len(csvGaiaXSimbad.header):])

                                            for key in csvDataOut.header:#[len(csvGaiaXSimbad.header):]:
                                                if key in csvGaiaXSDSS.header:
                                                    print('key = ',key)
                                                    for i in np.arange(0,len(posFoundInCsvOut),1):
                                                        if goodRun == 0:
                                                            csvDataOut.setData(key,posFoundInCsvOut[i],csvGaiaXSDSS.getData(key,goodStarsGaiaXSDSS[iStar]))
                                                        else:
                                                            posFound = -1
                                                            sourceId = csvGaiaXSDSS.getData(idKeyword,goodStarsGaiaXSDSS[iStar])
                                                            keywordPosOut = csvDataOut.findKeywordPos(idKeyword)
                                                            for iPosB in np.arange(0,len(rowsOut),1):
                                                                if rowsOut[iPosB][keywordPosOut] == sourceId:
                                                                    posFound = iPosB
                                                                    break
                                                            rowsOut[posFound][keywordPosOut] = csvGaiaXSDSS.getData(key,goodStarsGaiaXSDSS[iStar])
                                            print('csvDataOut.size() = ',csvDataOut.size())
                                            if goodRun == 1:
                                                csvDataOut.append(rowsOut)
                                                print('csvDataOut.size() = ',csvDataOut.size())
            #                                    STOP
                                    print('csvDataOut[',csvDataOut.size()-1,'] = ',csvDataOut.getData(csvDataOut.size()-1))
                        print('writing file <'+fnameOut+'>')
                        csvFree.writeCSVFile(csvDataOut, fnameOut)

if False:
    """cross-match GAIA x Simbad with GAIA x SDSS"""
    for iKeys in np.arange(0,len(keywordsToFindA),1):
        keysSimbad = keywordsToFindA[iKeys]
        keysSDSS = keywordsToFindB[iKeys]
        keyStrSimbad = keysSimbad[0][0]
        for key in keysSimbad[0][1:]:
            keyStrSimbad += '_'+key
        for key in keysSimbad[1:]:
            keyStrSimbad += '_'+key
        if True:#for iPix in np.arange(0,len(pixels),1):
            iPix = 34964
            fNameGaiaXSimbad = fNameARoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh, keyStrSimbad)
            print(iPix,': fNameGaiaXSimbad = <'+fNameGaiaXSimbad+'>')
            csvGaiaXSimbad = csvFree.readCSVFile(fNameGaiaXSimbad,',',True)
            if csvGaiaXSimbad.size() > 0:
                fNameGaiaXSDSS = fNameBRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh)
                print(iPix,': fNameGaiaXSDSS = <'+fNameGaiaXSDSS+'>')
                csvGaiaXSDSS = csvFree.readCSVFile(fNameGaiaXSDSS,',',True)
                if csvGaiaXSDSS.size() > 0:
                    for iStar in np.arange(0,csvGaiaXSDSS.size(),1):
                        posFound = csvGaiaXSDSS.find('source_id',csvGaiaXSDSS.getData('source_id',iStar),0)
                        if len(posFound) > 1:
                            print('PROBLEM: star with source_id ',csvGaiaXSDSS.getData('source_id',iStar),' found more than once at positions ',posFound)
                    STOP
                    process(iPix)
                    STOP

iPix = np.arange(0,len(pixels),1)
p = Pool(processes=16)
p.map(process, iPix)
p.close()
#for iPix in np.arange(0,len(pixels),1):
#    process(iPix)
