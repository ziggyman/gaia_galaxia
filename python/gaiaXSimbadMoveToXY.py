#! /usr/bin/env python

from multiprocessing import Pool
import os
import sys
import time
import numpy as np
import random

import csvData# for CSVData as a return type
import csvFree
import hammer
import moveStarsToXY

#globallock = Lock()


class GaiaXSimbad(object):
    ham = hammer.Hammer()
    inFileNames = []
    keys = []
    keyStr = ''
    releaseTractPatchCombinations = []
    fileWorkingName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/workinOnFiles.txt'
    fileWorking = None
    fileFinishedName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/finishedFiles.txt'
    fileFinished = None
    filesFinished = []
    filesWorking = []
    ids = ['source_id']
    logContent = []
    logFileName = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/gaiaXSimbadMoveToXY.log'

    def __init__(self):
        self.dir = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/'
        self.headerFile = os.path.join(self.dir, 'GaiaDR2xSimbad_aa')

    def openFileWorking(self, flag='a'):
        GaiaXSimbad.fileWorking = open(GaiaXSimbad.fileWorkingName, flag)

    def openFileFinished(self, flag='a'):
        GaiaXSimbad.fileFinished = open(GaiaXSimbad.fileFinishedName, flag)

    def closeFileWorking(self):
        GaiaXSimbad.fileWorking.close()

    def closeFileFinished(self):
        GaiaXSimbad.fileFinished.close()

    def writeToFileWorking(self, text):
        self.openFileWorking()
        GaiaXSimbad.fileWorking.write(text+'\n')
        self.closeFileWorking()

    def writeToFileFinished(self, text):
        self.openFileFinished()
        GaiaXSimbad.fileFinished.write(text+'\n')
        self.closeFileFinished()

    def readFinishedFiles(self):
        if os.path.isfile(GaiaXSimbad.fileFinishedName):
            self.openFileFinished(flag = 'r')
            lines = GaiaXSimbad.fileFinished.readlines()
            self.closeFileFinished()
            for line in lines:
                GaiaXSimbad.filesFinished.append(line[0:line.find(' ')])
            return True
        return False

    def readWorkingFiles(self):
        if os.path.isfile(GaiaXSimbad.fileWorkingName):
            self.openFileWorking(flag = 'r')
            lines = GaiaXSimbad.fileWorking.readlines()
            self.closeFileWorking()
            for line in lines:
                GaiaXSimbad.filesWorking.append(line[0:line.find('\n')])
            return True
        return False

    def readLogFile(self):
        if os.path.isfile(GaiaXSimbad.logFileName):
            logFile = open(GaiaXSimbad.logFileName, 'r')
            lines = logFile.readlines()
            logFile.close()
            for line in lines:
                lineSplit = line.split(' ')
                if lineSplit[0] == 'ran':
                    iIt = lineSplit[4]
                    fName = lineSplit[9]
                    if (fName in GaiaXSimbad.filesWorking) and (fName not in GaiaXSimbad.filesFinished):
                        fPos = -1
                        if len(GaiaXSimbad.logContent) > 0:
                            fNames = [GaiaXSimbad.logContent[i][0] for i in range(len(GaiaXSimbad.logContent))]
                            try:
                                fPos = fNames.index(fName)
                            except:
                                """do nothing"""
                        if fPos < 0:
                            GaiaXSimbad.logContent.append([fName, iIt])
                            fPos = len(GaiaXSimbad.logContent)-1
                        else:
                            GaiaXSimbad.logContent[fPos][1] = iIt
        else:
            GaiaXSimbad.logContent = [['a',-1]]

    def getInFileNames(self):
        if len(GaiaXSimbad.inFileNames) == 0:
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_aa"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ab"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ac"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ad"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ae"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_af"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ag"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ah"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ai"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_aj"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ak"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_al"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_am"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_an"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ao"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ap"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_aq"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ar"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_as"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_at"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_au"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_av"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_aw"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ax"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ay"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_az"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ba"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bb"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bc"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bd"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_be"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bf"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bg"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bh"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bi"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bj"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bk"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bl"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bm"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bn"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bo"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bp"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bq"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_br"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bs"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bt"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bu"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bv"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bw"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bx"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_by"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_bz"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ca"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cb"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cc"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cd"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ce"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cf"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cg"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ch"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ci"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cj"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ck"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cl"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cm"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cn"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_co"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cp"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cq"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cr"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cs"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ct"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cu"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cv"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cw"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cx"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cy"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_cz"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_da"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_db"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dc"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dd"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_de"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_df"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dg"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dh"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_di"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dj"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dk"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dl"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dm"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dn"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_do"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dp"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dq"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_dr"));
            GaiaXSimbad.inFileNames.append(self.dir + ("GaiaDR2xSimbad_ds"));

    def addXY(self, data):
        long = csvFree.convertStringVectorToDoubleVector(data.getData('l'))
        ind=np.where(long < 0.0)[0]
        if len(ind) > 0:
            print 'gaiaXSimbadMoveToXY.addXY: ind(where long < 0) = ',ind
            STOP
            long[ind]=long[ind] + 360.0

        lati = csvFree.convertStringVectorToDoubleVector(data.getData('b'))
        xys = GaiaXSimbad.ham.lonLatToXY(long, lati)

        data.addColumn(GaiaXSimbad.ham.getKeyWordHammerX(), xys[0])
        data.addColumn(GaiaXSimbad.ham.getKeyWordHammerY(), xys[1])

    def getHeader(self):

        GaiaXSimbad.keys = csvFree.readHeader(self.headerFile)
        GaiaXSimbad.keys.append(GaiaXSimbad.ham.getKeyWordHammerX())
        GaiaXSimbad.keys.append(GaiaXSimbad.ham.getKeyWordHammerY())

        GaiaXSimbad.keyStr = GaiaXSimbad.keys[0]
        for key in GaiaXSimbad.keys[1:]:
            GaiaXSimbad.keyStr += ','+key
        GaiaXSimbad.keyStr += '\n'
        return GaiaXSimbad.keys

    def writeHeaders(self):

        if len(GaiaXSimbad.keys) == 0:
            self.getHeader()

        pixels = GaiaXSimbad.ham.getPixels()
        print 'type(GaiaXSimbad.keys) = ',type(GaiaXSimbad.keys),': ',type(GaiaXSimbad.keys[0])
        print 'type(pixels) = ',type(pixels),': ',type(pixels[0])
        whichone = 'gaiaXSimbad'
        whichone = whichone.decode('utf-8')
        print 'type(whichone) = ',type(whichone)
        print 'type("gaiaXSimbad") = ',type('gaiaXSimbad')
        print 'type(False) = ',type(False)
        tempdir = ''
        tempdir = tempdir.decode('utf-8')
        moveStarsToXY.writeHeaderToOutFiles(GaiaXSimbad.keys,
                                            pixels,
                                            whichone,
                                            False,
                                            tempdir)

    def processGaiaXSimbad(self, iCombo):
        doIt = True
        inputFile = ''

        pixels = GaiaXSimbad.ham.getPixels()

        if doIt:
            timeStart = time.time()
            inputFile = GaiaXSimbad.inFileNames[iCombo]
            if not os.path.isfile(inputFile):
                print "gaiaXSimbadMoveToXY.processGaiaXSimbad: ERROR: gaiaXSimbad input file ",inputFile," not found"
                STOP

            data = csvFree.readCSVFile(inputFile)

            # add Hammer x and y
            self.addXY(data)

            moveStarsToXY.appendCSVDataToXYFiles(data,
                                                 pixels,
                                                 'gaiaXSimbad',
                                                 GaiaXSimbad.ids,
                                                 False,
                                                 '',
                                                 '')
            timeEnd = time.time()
            duration = timeEnd-timeStart
            print 'gaiaXSimbadMoveToXY.processGaiaXSimbad: ran file <', inputFile,'> in ',duration,' seconds'

            self.writeToFileFinished(inputFile+' done in '+str(duration)+'s')

    #        globallock.release()
def processGaiaXSimbad(iCombo):
    gal = GaiaXSimbad()
    gal.processGaiaXSimbad(iCombo)

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    gal = GaiaXSimbad()
    gal.getInFileNames()
    gal.getHeader()
    gal.writeHeaders()
    if not gal.readWorkingFiles():
        gal.openFileWorking('w')
        gal.closeFileWorking()
    if not gal.readFinishedFiles():
        gal.openFileFinished('w')
        gal.closeFileFinished()
    gal.readLogFile()

    folder = '/var/lock'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    if True:
        p = Pool(processes=16)
        iCombo = np.arange(len(GaiaXSimbad.inFileNames))
        #gal.processGaiaXSimbad(iCombo[0])
        random.shuffle(iCombo)
        p.map(processGaiaXSimbad, iCombo)
        p.close()

if __name__ == '__main__':
    main(sys.argv)
