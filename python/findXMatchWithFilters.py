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
    print data.header

main()
