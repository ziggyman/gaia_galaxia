import csv
import csvData
import csvFree
import hammer
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn import linear_model

from gaiaxsimbad import calcY,getGiantsAndDwarfs,getGoodStarIndices,getXY

colorSystems = ['Johnson_Cousins','ugriz']

#GaiaDR2+Simbad+SDSS/xy/GaiaXSimbad+SDSS_2.793072-2.810749_0.141421-0.159099_u_g_r_umag_gmag_rmag_phot_bp_mean_mag_rv_template_logg.csv
fNameGaiaXSimbad_and_SDSS_root = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2+Simbad+SDSS/xy/GaiaXSimbad+SDSS_%.6f-%.6f_%.6f-%.6f_%s.csv'

#required x values for certain GAIA passband
xForGBP = [['g','gmag'],['r','rmag'],'phot_bp_mean_mag','rv_template_logg']
#xForGBP = [['u','umag'],['g','gmag'],['r','rmag'],'phot_bp_mean_mag','rv_template_logg']
xForGRP = [['r','rmag'],['i','imag'],['z','zmag'],'phot_rp_mean_mag','rv_template_logg']

xForGBP_Jc = [['B','SimbadB'],['V','SimbadV'],['R','SimbadR'],'phot_bp_mean_mag','rv_template_logg']
xForGRP_Jc = [['R','SimbadR'],['I','SimbadI'],'phot_rp_mean_mag','rv_template_logg']

ham = hammer.Hammer()
pixels = ham.getPixels()

def getGoodStarIndices(csvIn, requiredKeywords):
    indicesOut = []
    for iStar in range(csvIn.size()):
        isGood = True
        for iKey in range(len(requiredKeywords)):
            if isGood:
                if len(requiredKeywords[iKey]) < 3:#['umag','u']
                    if (csvIn.getData(requiredKeywords[iKey][0], iStar) == '') and (csvIn.getData(requiredKeywords[iKey][1], iStar) == ''):
                        print('csvIn.getData(',requiredKeywords[iKey][0],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][0], iStar),
                              '> csvIn.getData(',requiredKeywords[iKey][1],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][1], iStar),
                              '> => NOT GOOD')
                        isGood = False
                    else:
                        print('csvIn.getData(',requiredKeywords[iKey][0],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][0], iStar),
                              '> csvIn.getData(',requiredKeywords[iKey][1],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][1], iStar),
                              '> => IS GOOD')
                else:
                    if csvIn.getData(requiredKeywords[iKey], iStar) == '':
                        print('csvIn.getData(',requiredKeywords[iKey],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey], iStar),'> => NOT GOOD')
                        isGood = False
                    else:
                        print('csvIn.getData(',requiredKeywords[iKey],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey], iStar),'> => STILL GOOD')
        if isGood:
            indicesOut.append(iStar)
            print('getGoodStarIndices: found a good star at pos ',iStar)
        else:
            print('getGoodStarIndices: found a bad star at pos ',iStar)
    print('getGoodStarIndices: ',len(indicesOut),' out of ',csvIn.size(),' are good')
    return indicesOut

def getXY(csvIn, requiredKeywords, indicesIn, nDegree):
    x = []
    y = []
    nBoth = 0
    both = []
    for iStar in indicesIn:
        xStar = [1.0]
        for iKey in range(len(requiredKeywords)):
            if len(requiredKeywords[iKey]) < 3:#['umag','u']
                if (csvIn.getData(requiredKeywords[iKey][0], iStar) != '') and (csvIn.getData(requiredKeywords[iKey][1], iStar) != ''):
                    xMean = np.mean([float(csvIn.getData(requiredKeywords[iKey][0], iStar)),float(csvIn.getData(requiredKeywords[iKey][1], iStar))])
#                    print('csvIn.getData(',requiredKeywords[iKey][0],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][0], iStar),
#                          '> csvIn.getData(',requiredKeywords[iKey][1],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][1], iStar),
#                          '> => mean = ',xMean)
                    xTemp = xMean
                    nBoth += 1
                    both.append([csvIn.getData(requiredKeywords[iKey][0], iStar), csvIn.getData(requiredKeywords[iKey][1], iStar)])
                elif csvIn.getData(requiredKeywords[iKey][0], iStar) != '' and csvIn.getData(requiredKeywords[iKey][1], iStar) == '':
#                    print('csvIn.getData(',requiredKeywords[iKey][0],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][0], iStar),
#                          '> csvIn.getData(',requiredKeywords[iKey][1],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][1], iStar),
#                          '> => x = ',csvIn.getData(requiredKeywords[iKey][0], iStar))
                    xTemp = float(csvIn.getData(requiredKeywords[iKey][0], iStar))
                elif csvIn.getData(requiredKeywords[iKey][0], iStar) == '' and csvIn.getData(requiredKeywords[iKey][1], iStar) != '':
#                    print('csvIn.getData(',requiredKeywords[iKey][0],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][0], iStar),
#                          '> csvIn.getData(',requiredKeywords[iKey][1],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey][1], iStar),
#                          '> => x = ',csvIn.getData(requiredKeywords[iKey][1], iStar))
                    xTemp = float(csvIn.getData(requiredKeywords[iKey][1], iStar))
                else:
                    print("don't know what to do")
                    STOP
                for iDeg in np.arange(1,nDegree+1):
                    xStar.append(xTemp ** iDeg)
            else:
                y.append(float(csvIn.getData(requiredKeywords[iKey], iStar)))
#                print('csvIn.getData(',requiredKeywords[iKey],', ',iStar,') = <',csvIn.getData(requiredKeywords[iKey], iStar),'> = y')
        x.append(xStar)
    print('nBoth = ',nBoth)
    print('both = ',both)
    return [x,y]

with open(fNameGaiaXSimbad_and_SDSS_root[:fNameGaiaXSimbad_and_SDSS_root.rfind('/')+1]+'results.txt','w') as f:
    for xKeys in [xForGBP,xForGRP]:
        suffix = ''
        for iKeyRun in range(2):
            for iKey in range(len(xKeys)):
                if len(xKeys[iKey]) > 2:
                    if iKeyRun == 1:
                        suffix += '_'+xKeys[iKey]
                else:
                    suffix += '_'+xKeys[iKey][iKeyRun]
        suffix = suffix[1:]
        print('suffix = <'+suffix+'>')

        fNameOut = fNameGaiaXSimbad_and_SDSS_root[:fNameGaiaXSimbad_and_SDSS_root.rfind('/')+1]+'GaiaXSimbad+SDSS_'+suffix+'.csv'
        csvGood = None
        if not os.path.isfile(fNameOut):
            csvGood = csvData.CSVData()
            headerSet = False
            nStars = 0
            for pix in pixels:
                inFile = fNameGaiaXSimbad_and_SDSS_root % (pix.xLow, pix.xHigh, pix.yLow, pix.yHigh, suffix)
                print('reading inFile <'+inFile+'>')
                csvIn = csvFree.readCSVFile(inFile,',',True)
                if not headerSet:
                    csvGood.header = csvIn.header
                    headerSet = True
                print('csvIn.size() = ',csvIn.size())
                print('len(csvIn.data) = ',len(csvIn.data))
                if csvIn.size() > 0:
                    nStars += csvIn.size()
                    goodStarIndices = getGoodStarIndices(csvIn, xKeys)
                    print('goodStarIndices = ',goodStarIndices)
                    if len(goodStarIndices) > 0:
                        csvGood.append(csvIn.getData(goodStarIndices))
                        print('csvGood.size() = ',csvGood.size())

            csvFree.writeCSVFile(csvGood, fNameOut)
            print(csvGood.size(),' good stars out of ',nStars)

        else:
            csvGood = csvFree.readCSVFile(fNameOut,',',True)

        dwarfs, giants = getGiantsAndDwarfs(csvGood, range(csvGood.size()))
        print('len(dwarfs) = ',len(dwarfs),'len(giants) = ',len(giants))

        for nDegree in [1,2,3,4,5,6]:

            xDwarfs, yDwarfs = getXY(csvGood, xKeys[:len(xKeys)-1], dwarfs, nDegree)
        #    print('xDwarfs = ',len(xDwarfs),': ',xDwarfs)
        #    print('yDwarfs = ',len(yDwarfs),': ',yDwarfs)
            xGiants, yGiants = getXY(csvGood, xKeys[:len(xKeys)-1], giants, nDegree)
        #    print('xGiants = ',len(xGiants),': ',xGiants)
        #    print('yGiants = ',len(yGiants),': ',yGiants)

            yKey = xKeys[3]
            xKeysOne = [x[0] for x in xKeys[0:3]]
            for stars in ['dwarfs', 'giants']:
                print('Calculating '+stars)
                indicesTemp = None
                xDat = None
                yDat = None
                if stars == 'dwarfs':
                    indicesTemp = dwarfs
                    xDat = xDwarfs
                    yDat = yDwarfs
                    print('indicesTemp set to dwarfs')
                else:
                    indicesTemp = giants
                    xDat = xGiants
                    yDat = yGiants
                    print('indicesTemp set to giants')

                print('indicesTemp = ',len(indicesTemp),': ',indicesTemp)
                x = []
                xTest = []
                y = []
                yTest = []
                indices = []
                indicesTest = []
                for k in np.arange(0,len(indicesTemp),1):
                    print('k = ',k)
                    if float(k) / 100. == int(float(k)/100.):#use as test data
                        xTest.append(xDat[k])
                        yTest.append(yDat[k])
                        indicesTest.append(k)
                        print('k = ',k,': xDat[',k,'] = ',xDat[k],' added to xTest, yDat[',k,'] added to yTest, ',k,' added to indicesTest')
                    else:
                        x.append(xDat[k])
                        y.append(yDat[k])
                        indices.append(k)
                        print('k = ',k,': xDat[',k,'] = ',xDat[k],' added to x, yDat[',k,'] added to y, ',k,' added to indices')

                print('x = ',x)
                print('y = ',y)
                print('indices = ',indices)
                print('xTest = ',xTest)
                print('yTest = ',yTest)
                print('indicesTest = ',indicesTest)
                print('len(x) = ',len(x),', len(y) = ',len(y),', len(indices) = ',len(indices))
                print('len(xTest) = ',len(xTest),', len(yTest) = ',len(yTest),', len(indicesTest) = ',len(indicesTest))

                #clf = linear_model.LinearRegression(fit_intercept=False, normalize=False, copy_X=True)
                #clf.fit(x, y)
                print('before lstsq: x = ',x)
                print('before lstsq: y = ',y)
                clf = np.linalg.lstsq(x,y)#[0]
                #print 'dir(clf) = ',dir(clf)
                #print 'type(clf) = ',type(clf)
                #print 'clf = ',clf
                coeffs = clf[0]
                print('============================== coeffs = ',coeffs)
                #print 'clf.get_params = ',clf.get_params

                if True:
                    """check fit on our input data"""
                    yCalc = calcY(x, clf[0])
                    yDiff = np.array(y) - np.array(yCalc)
                    print('len(yDiff) = ',len(yDiff))
                    #print 'yDiff = ',yDiff
                    mean = np.mean(yDiff)
                    stdev = np.std(yDiff)
                    print('mean = ',mean,', stdev = ',stdev)
                    dist = []
                    for i in range(len(indices)):
                        dist.append(float(csvGood.getData('angDist', indices[i])))
                #    plt.xlabel('angular distance')
                #    plt.ylabel('G_BP difference')
                #    plt.show()


                if True:
                    """check fit on neighbouring field"""
                    print('testing '+stars+' with ',len(indicesTest),' stars')

                    yCalc = calcY(xTest, clf[0])
                    #print 'yCalc = ',yCalc
                    yDiffTest = np.array(yTest) - np.array(yCalc)
                    #print 'yDiffTest = ',yDiffTest
                    mean = np.mean(yDiffTest)
                    stdev = np.std(yDiffTest)
                    print('test mean = ',mean,', stdev = ',stdev)

                    th = 'th'
                    if nDegree == 1:
                        th = 'st'
                    elif nDegree == 2:
                        th = 'nd'

                    distTest = []
                    for i in range(len(indicesTest)):
                        distTest.append(float(csvGood.getData('angDist', indicesTest[i])))
                    plt.scatter(dist, yDiff, c='b')
    #                print('len(distTest) = ',len(distTest))
    #                print('len(yDiffTest) = ',len(yDiffTest))
                    plt.scatter(distTest, yDiffTest, c='g')
                    plt.xlabel('angular distance')
                    if yKey == 'phot_bp_mean_mag':
                        plt.ylabel('G_BP difference (measured - calcuated)')
                    elif yKey == 'phot_rp_mean_mag':
                        plt.ylabel('G_RP difference (measured - calcuated)')
                    title = stars + ' ' + str(nDegree) + th + ' degree polynomial'
                    plt.title(title)
                    plotname = fNameGaiaXSimbad_and_SDSS_root[:fNameGaiaXSimbad_and_SDSS_root.rfind('/')+1]
                    for xKey in xKeysOne:
                        plotname += xKey
                    plotname += '_'+yKey+'_'+stars+'_'+str(nDegree)+th+'Degree'
                    plotname += '.pdf'
                    plt.savefig(plotname, format='pdf', frameon=False, bbox_inches='tight', pad_inches=0.1)
                    plt.show()

                    plt.scatter(yTest, yCalc, c='b')
                    plt.plot([np.min(yTest)-0.5, np.max(yTest)+0.5],[np.min(yTest)-0.5, np.max(yTest)+0.5])
                    plt.xlim([np.min(yTest)-0.5, np.max(yTest)+0.5])
                    plt.ylim([np.min(yTest)-0.5, np.max(yTest)+0.5])
    #                print('len(distTest) = ',len(distTest))
    #                print('len(yDiffTest) = ',len(yDiffTest))
    #                plt.scatter(distTest, yDiffTest, c='g')
                    if yKey == 'phot_bp_mean_mag':
                        plt.xlabel('G_BP measured')
                        plt.ylabel('G_BP calcuated')
                    elif yKey == 'phot_rp_mean_mag':
                        plt.xlabel('G_RP measured')
                        plt.ylabel('G_RP calcuated')
                    title = stars+' '+str(nDegree)+th+' degree polynomial'
                    plt.title(title)
                    plotname = fNameGaiaXSimbad_and_SDSS_root[:fNameGaiaXSimbad_and_SDSS_root.rfind('/')+1]
                    for xKey in xKeysOne:
                        plotname += xKey
                    plotname += '_'+yKey+'_'+stars+'_'+str(nDegree)+th+'Degree'
                    plotname += '_calc_vs_Gaia.pdf'
                    plt.savefig(plotname, format='pdf', frameon=False, bbox_inches='tight', pad_inches=0.1)
                    plt.show()

                    f.write(plotname+': mean difference = '+str(mean)+', stddev = '+str(stdev)+'\n')

    #                STOP
