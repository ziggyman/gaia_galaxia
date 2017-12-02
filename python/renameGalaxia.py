#! /usr/bin/env python
import os
import sys

import numpy as np

def main(argv):
    """Main program.

    Arguments:
    argv -- command line arguments
    """
    lon_old = np.arange(-175, 0, 10)
    lon_new = lon_old + 360
    print 'lon_old = ',lon_old,', lon_new = ',lon_new
    lats = np.arange(-85, 90, 10)
    bashCommandParameterFileRoot = 'mv /Volumes/yoda/azuri/data/galaxia/parameterfile_%d_%d /Volumes/yoda/azuri/data/galaxia/parameterfile_%d_%d'
    bashCommandGalaxiaFileRoot = 'mv /Volumes/yoda/azuri/data/galaxia/galaxia_%d-%d_%d-%d.csv /Volumes/yoda/azuri/data/galaxia/galaxia_%d-%d_%d-%d.csv'
    for iLon in range(len(lon_old)):
        for lat in lats:
            bashCommandParameterFile = bashCommandParameterFileRoot % (
                                       lon_old[iLon], lat, lon_new[iLon], lat)
            bashCommandGalaxiaFile = bashCommandGalaxiaFileRoot % (
                                     lon_old[iLon]-5,
                                     lon_old[iLon]+5,
                                     lat-5,
                                     lat+5,
                                     lon_new[iLon]-5,
                                     lon_new[iLon]+5,
                                     lat-5,
                                     lat+5)
            print 'bashCommandParameterFile = ',bashCommandParameterFile
            print 'bashCommandGalaxiaFile = ',bashCommandGalaxiaFile
#            os.system(bashCommandParameterFile)
#            os.system(bashCommandGalaxiaFile)

if __name__ == '__main__':
    main(sys.argv)

