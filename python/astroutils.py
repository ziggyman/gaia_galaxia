from astropy import units as u
from astropy.coordinates import SkyCoord
import csv
import numpy as np

# convert ra and dec (degrees) to ICRS (FK5 epoch=2000) l and b
def radec2lb(ra, dec):
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    return c.galactic

def readCSVHeader(filename):
    with open(filename) as f:
        header = f.readline().rstrip().split(',')
    return header

def readCSVFileToDict(filename):
    with open(filename) as csvfile:
        dic = csv.DictReader(csvfile)
    return dic

def writeDictToCSVFile(dic, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dic.keys)

        writer.writeheader()
        for row in dic:
            writer.writerow(row)

def readCSVToDict(filename):
    reader = csv.reader(open(filename, 'r'))
    d = {}

    iLine = 0
    keys = []
    values = []
    for row in reader:
        if iLine == 0:
            keys = row
            print len(keys),' keys found'
        else:
            values.append(row)
        iLine += 1

    data = {}
    for i in range(len(keys)):
        data[keys[i]] = [value[i] for value in values]

    return data

def writeDictToCSV(dic, filename, header=None):
    if not header:
        keys = dic.keys()
    else:
        keys = header
    with open(filename,'w') as f:
        str = keys[0]
        for i in np.arange(1,len(keys)):
            str += ','+keys[i]
        f.write(str+'\n')
        nDataLines = len(dic[keys[0]])
        for line in range(nDataLines):
            str = dic[keys[0]][line]
            for i in np.arange(1,len(keys)):
                str += ','+dic[keys[i]][line]
            f.write(str+'\n')

def add_lb_to_csv_file(fname_in, ra_key, dec_key, fname_out = None):
    dic = readCSVToDict(fname_in)
    header = readCSVHeader(fname_in)
    print 'header = ',header

    ra = [float(i) for i in dic[ra_key]]
    dec = [float(i) for i in dic[dec_key]]

    lb = radec2lb(ra, dec)
#        lb = radec2lb(91.61798222751897, 64.92579518769703)#149.15740521759471,19.845469389765825
#        l.append(float(lb.l/u.degree))
#        b.append(float(lb.b/u.degree))

    dic['l'] = [str(float(lbi.l/u.degree)) for lbi in lb]
    dic['b'] = [str(float(lbi.b/u.degree)) for lbi in lb]

    header.append('l')
    header.append('b')

#    l = lb[:][0]
#    b = lb[:][1]

#    print 'l = ',l
#    print 'b = ',b

    if fname_out is None:
        fname_out = fname_in
    writeDictToCSV(dic, fname_out, header)

def addHeader(filename, header):
    lines = []
    with open(filename) as f:
        lines = f.readlines()
    headerstr = header[0]
    for i in np.arange(1,len(header)):
        headerstr += ','+header[i]
    headerstr += '\n'
    with open(filename, 'w') as f:
        f.write(headerstr)
        for line in lines:
            f.write(line)
