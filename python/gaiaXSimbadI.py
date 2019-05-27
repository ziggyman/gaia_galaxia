import os

import matplotlib.pyplot as plt
import numpy as np

import csvData
import csvFree
import hammer

#parameters
pathOut = '/Volumes/obiwan/azuri/data/gaia/x-match/simbadI/xy/'
#fnameList = path+'xyfiles.list'

fNameGaiaXSimbad = '/Volumes/obiwan/azuri/data/gaia/x-match/simbadI/simbad_ImagXGaia.csv'
fnameOutRoot = os.path.join(pathOut,'GaiaXSimbadI_%.6f-%.6f_%.6f-%.6f_%s.csv')

nStarsDone = 0
ham = hammer.Hammer()
pixels = ham.getPixels()

keywordsToFindSimbad = [[['SimbadB','SimbadV','SimbadR'],'phot_bp_mean_mag','rv_template_logg'],
                        [['SimbadB','SimbadV'],'phot_bp_mean_mag','rv_template_logg'],
                        [['SimbadR','SimbadI'],'phot_rp_mean_mag','rv_template_logg'],
                        [['SimbadB','SimbadV','SimbadR','SimbadI'],'phot_g_mean_mag','rv_template_logg'],
                       ]
keywordsToFindGaia = [[['B','V','R'],'phot_bp_mean_mag','rv_template_logg'],
                      [['B','V'],'phot_bp_mean_mag','rv_template_logg'],
                      [['R','I'],'phot_rp_mean_mag','rv_template_logg'],
                     [['B','V','R','I'],'phot_g_mean_mag','rv_template_logg'],
                      ]

# data: dictionary
def getGoodStarIndices(data, keywords):
#    print('getGoodStarIndices: data.header = ',data.header)
#    print('getGoodStarIndices: keywords = <',keywords,'>')
    goodStars = []

    cols = []
    for keyword in keywords[0]:
#        print('getGoodStarIndices: keyword = <',keyword,'>')
        if keyword in data.header:
            cols.append(data.getData(keyword))
        else:
            cols.append('' for x in range(data.size()))
    for keyword in keywords[1:]:
#        print('getGoodStarIndices: keyword = <',keyword,'>')
        cols.append(data.getData(keyword))

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

def process(iPix):

    if True:#not os.path.isfile(fnameOut):

        """get indices of stars which have data for all required keys"""
#        print('searching for stars with all needed parameters')
        for iKeys in range(len(keywordsToFindSimbad)):
            print('iKeys = ',iKeys)
            keysSimbad = keywordsToFindSimbad[iKeys]
            keysGaia = keywordsToFindGaia[iKeys]

            keyStr = keysSimbad[0][0]
            for key in keysSimbad[0][1:]:
                keyStr += '_'+key
            for key in keysGaia[0]:
                keyStr += '_'+key
            for key in keysSimbad[1:]:
                keyStr += '_'+key

            fnameOut = fnameOutRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh, keyStr)

            if not os.path.isfile(fnameOut):
                keyStrSimbad = keysSimbad[0][0]
                for key in keysSimbad[0][1:]:
                    keyStrSimbad += '_'+key
                for key in keysSimbad[1:]:
                    keyStrSimbad += '_'+key
                fNameGaiaXSimbad = fNameGaiaXSimbadRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh, keyStrSimbad)
    #            print('fNameGaiaXSimbad = <'+fNameGaiaXSimbad+'>')
                csvGaiaXSimbad = csvFree.readCSVFile(fNameGaiaXSimbad,',',True)
                print('csvGaiaXSimbad.header = ',len(csvGaiaXSimbad.header),': ',csvGaiaXSimbad.header)
                print(' ')

                fNameGaiaXGaia = fNameGaiaXSDSSRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh)
    #            print('fNameGaiaXSDSS = <'+fNameGaiaXSDSS+'>')
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

                goodStarsGaiaXSimbad = getGoodStarIndices(csvGaiaXSimbad, keywordsToFindSimbad[iKeys])
                print('found ',len(goodStarsGaiaXSimbad),' good stars out of ',csvGaiaXSimbad.size(),' stars')
                print('goodStarsGaiaXSimbad = ',goodStarsGaiaXSimbad)
                rowsOut = []
                if len(goodStarsGaiaXSimbad) > 0:
                    rowsOut = csvGaiaXSimbad.getData(goodStarsGaiaXSimbad)
                    print('len(goodStarsGaiaXSimbad) > 0: len(rowsOut) = ',len(rowsOut),', len(rowsOut[0]) = ',len(rowsOut[0]))
                    for iKey in np.arange(len(csvGaiaXSimbad.header), len(csvDataOut.header),1):
                        print('iKey = ',iKey)
                        for iRowOut in range(len(rowsOut)):
                            rowsOut[iRowOut].append('')
                            print('len(rowsOut[',iRowOut,']) = ',len(rowsOut[iRowOut]))
                print('rowsOut = ',len(rowsOut))
                if len(rowsOut) > 0:
                    print('len(rowsOut[0]) = ',len(rowsOut[0]))
                    if len(rowsOut[0]) != len(csvDataOut.header):
                        print('ERROR: len(rowsOut[0])=',len(rowsOut[0]),' != len(csvDataOut.header)=',len(csvDataOut.header))
                isBad = False
                for iRrow in range(len(rowsOut)):
                    if len(rowsOut[iRrow]) != len(csvDataOut.header):
                        print('ERROR: len(rowsOut[',iRrow,'])=',len(rowsOut[iRrow]),' != len(csvDataOut.header)=',len(csvDataOut.header))
                        isBad = True
                if isBad:
                    STOP
                if len(rowsOut) > 0:
                    csvDataOut.data = rowsOut

    #            print('csvGaiaXSimbad.getData(0)[0] = ',csvGaiaXSimbad.getData(0)[0])
    #            print('csvGaiaXSimbad.getData(',csvGaiaXSimbad.header[0],',0) = ',csvGaiaXSimbad.getData(csvGaiaXSimbad.header[0],0))
    #            STOP


                goodStarsGaiaXSDSS = getGoodStarIndices(csvGaiaXSDSS, keywordsToFindSDSS[iKeys])
                print('len(goodStarsGaiaXSDSS) = ',len(goodStarsGaiaXSDSS))
                for iStar in range(len(goodStarsGaiaXSDSS)):
                    print('iStar = ',iStar)
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
                                for i in range(len(posFoundInCsvOut)):
                                    csvDataOut.setData(key,posFoundInCsvOut[i],csvGaiaXSDSS.getData(key,goodStarsGaiaXSDSS[iStar]))
                    print('csvDataOut[',csvDataOut.size()-1,'] = ',csvDataOut.getData(csvDataOut.size()-1))
                print('writing file <'+fnameOut+'>')
                csvFree.writeCSVFile(csvDataOut, fnameOut)

if False:
    """cross-match GAIA x Simbad with GAIA x SDSS"""
    for iKeys in range(len(keywordsToFindSimbad)):
        keysSimbad = keywordsToFindSimbad[iKeys]
        keysSDSS = keywordsToFindSDSS[iKeys]
        keyStrSimbad = keysSimbad[0][0]
        for key in keysSimbad[0][1:]:
            keyStrSimbad += '_'+key
        for key in keysSimbad[1:]:
            keyStrSimbad += '_'+key
        if True:#for iPix in range(len(pixels)):
            iPix = 34964
            fNameGaiaXSimbad = fNameGaiaXSimbadRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh, keyStrSimbad)
            print(iPix,': fNameGaiaXSimbad = <'+fNameGaiaXSimbad+'>')
            csvGaiaXSimbad = csvFree.readCSVFile(fNameGaiaXSimbad,',',True)
            if csvGaiaXSimbad.size() > 0:
                fNameGaiaXSDSS = fNameGaiaXSDSSRoot % (pixels[iPix].xLow, pixels[iPix].xHigh, pixels[iPix].yLow, pixels[iPix].yHigh)
                print(iPix,': fNameGaiaXSDSS = <'+fNameGaiaXSDSS+'>')
                csvGaiaXSDSS = csvFree.readCSVFile(fNameGaiaXSDSS,',',True)
                if csvGaiaXSDSS.size() > 0:
                    for iStar in range(csvGaiaXSDSS.size()):
                        posFound = csvGaiaXSDSS.find('source_id',csvGaiaXSDSS.getData('source_id',iStar))
                        if len(posFound) > 1:
                            print('PROBLEM: star with source_id ',csvGaiaXSDSS.getData('source_id',iStar),' found more than once at positions ',posFound)
                    STOP
                    process(iPix)
                    STOP

iPix = range(len(pixels))
p = Pool(processes=16)
p.map(process, iPix)
p.close()
#for iPix in range(len(pixels)):
#    process(iPix)
