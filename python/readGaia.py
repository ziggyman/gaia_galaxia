#! /usr/bin/env python
import csv
import csvData
import csvFree

#fname = '/Volumes/external/azuri/data/gaia/GaiaSource_1008431284282695936_1008626993058019840.csv'
fname = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad.csv'


def readGaiaToDict(filename):
    reader = csv.reader(open(filename, 'r'))
    d = {}

    iLine = 0
    keys = []
    values = []
    for row in reader:
        if iLine == 0:
            keys = row
            print len(keys)
        else:
            values.append(row)
        iLine += 1
    print len(values)
    print values[0]

    data = {}
    for i in range(len(keys)):
        data[keys[i]] = [value[i] for value in values]

    print 'data[',keys[0],'] = ',data[keys[0]]
    print 'data[ra] = ',data['ra']
    return data

def readGaiaCSVData():
    return csvFree.readCSVFile(fname)

def main():
    data = readGaiaCSVData()
    print 'size = ',data.size()
    print data.getData('ra')

main()
