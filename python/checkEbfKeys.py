#! /usr/bin/env python

import ebf
from glob import glob
import sys

def main(args):
    keysA = []
    iFile = 0
    cache = 1
    for filename in glob("/Volumes/external/azuri/data/galaxia/sdss/*.ebf"):
        print 'checking filename ',filename
        data = ebf.iterate(filename, '/px+', cache)
        for it in data:
            keys = it.keys()
            break
        if iFile == 0:
            keysA = keys
            iFile+=1
        else:
            for key, keyA in zip(keys, keysA):
                if key != keyA:
                    raise Exception('ERROR: key(=',key,') != keyA(=',keyA,')')
    print 'passed'

if __name__ == '__main__':
    main(sys.argv)
