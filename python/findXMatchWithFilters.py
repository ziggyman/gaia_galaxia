#! /usr/bin/env python
import csv
import csvData
import csvFree

fname = '/Volumes/obiwan/azuri/data/gaia/GaiaDR2xSimbad.csv'

def readGaiaCSVData():
    return csvFree.readCSVFile(fname)

def main():
    data = readGaiaCSVData()
    print 'size = ',data.size()

    print 'data.header = ',data.header

    print 'data.header[0] = ',data.header[0]
    print 'type(data.header[0]) = ',type(data.header[0])
    print 'type(u"U") = ',type(u'U')

    b = data.getData(u'B')
    v = data.getData(u'V')
    r = data.getData(u'R')

    newData = csvData.CSVData()
    newData.header = data.header

    for pos in range(len(b)):
        if ((b[pos] != '')
            and (v[pos] != '')
            and (r[pos] != '')):
            newData.append(data.getData(pos))

    print 'len(newData.data) = ',len(newData.data)

main()
