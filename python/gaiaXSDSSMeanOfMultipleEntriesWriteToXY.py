from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import sys, traceback

import csvData#2 as csvData
import csvFree#2 as csvFree
import hammer#2 as hammer
import moveStarsToXY#2 as moveStarsToXY
#from myUtils import getStarWithMinDist

filename = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/1552971988347A.csv'#'/Volumes/obiwan/azuri/data/lamost/dr7_med_v0_q1.csv'
outFilename = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/GaiaXSDSS_xy.csv'

ham = hammer.Hammer()
pixels = ham.getPixels()

csv = None
try:
    csv = csvFree.readCSVFile(filename, ',', True)
except:
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

def writeToXY(csv):
    ra = [float(a) for a in csv.getData('RA_ICRS')]
    dec = [float(a) for a in csv.getData('DE_ICRS')]
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    gal = c.galactic
    csv.addColumn('l',[str(a.value) for a in gal.l])
    csv.addColumn('b',[str(a.value) for a in gal.b])

    xy = ham.lonLatToXY(csvFree.convertStringVectorToDoubleVector(csv.getData('l')),csvFree.convertStringVectorToDoubleVector(csv.getData('b')))
#    print('iStar = ',i,': ra = ',ra,', dec = ',dec,': l = ',gal.l.value,', b = ',gal.b.value)#,': x = ',xy.x,', y = ',xy.y)
#    csv.addColumn('l')
#    csv.addColumn('b')
    csv.addColumn(ham.getKeyWordHammerX(), [str(a) for a in xy[0]])
    csv.addColumn(ham.getKeyWordHammerY(), [str(a) for a in xy[1]])
#    for i in range(csv.size()):
#        csv.setData(ham.getKeyWordHammerX(),i,xy.x)
#        csv.setData(ham.getKeyWordHammerX(),i,xy.y)
    csvFree.writeCSVFile(csv,outFilename)
    return csv
#        STOP

print('csv.size() = ',csv.size())

try:
    print('combining multiple entries')
    idKey = "source_id"
    print('key = <'+idKey+'>')
    keysToCombine = ['umag','gmag','rmag','imag','zmag']
    csvMean = csv.combineMultipleEntries('source_id', ['umag','gmag','rmag','imag','zmag'])#idKey,keysToCombine)
    print('multiple entries combined')
except:
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

csvMean = writeToXY(csvMean)

#void writeHeaderToOutFiles(vector<string> const& header,
#                           vector<Pixel> const& pixels,
#                           string const& whichOne,
#                           bool const& append,
#                           string const& dataDirOut = "");
moveStarsToXY.writeHeaderToOutFiles(csvMean.header,
                                    pixels,
                                    'gaiaXSDSS',
                                    False,
                                    '')

#int appendCSVDataToXYFiles(CSVData const& csvData,
#                            vector<Pixel> const& pixels,
#                            string const& whichOne,
#                            vector<string> const& ids,
#                            bool const& doFind=false,
#                            string const& lockSuffix="",
#                            string const& outputDir="");
moveStarsToXY.appendCSVDataToXYFiles(csvMean,
                                     pixels,
                                     'gaiaXSDSS',
                                     ['source_id'],
                                     False,
                                     '',
                                     '')

