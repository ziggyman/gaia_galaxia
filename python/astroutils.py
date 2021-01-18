from astropy import units as u
from astropy.coordinates import SkyCoord
import csv
import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt
import rpy2.robjects as R

import hammer
import csvFree,csvData
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
            print(len(keys),' keys found')
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
    print('header = ',header)

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

#    print(''l = ',l
#    print(''b = ',b

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

def add_xy_to_csv_file(fname_in, l_key, b_key, x_key, y_key, fname_out = None):
    dic = readCSVToDict(fname_in)
    header = readCSVHeader(fname_in)
    print('header = ',header)

    l = [float(i) for i in dic[l_key]]
    b = [float(i) for i in dic[b_key]]

    ham = hammer.Hammer()

    xy = ham.lonLatToXY(l, b)
#        lb = radec2lb(91.61798222751897, 64.92579518769703)#149.15740521759471,19.845469389765825
#        l.append(float(lb.l/u.degree))
#        b.append(float(lb.b/u.degree))

    print('type(xy) = ',type(xy))
    print('len(xy) = ',len(xy))
    print('type(xy[0]) = ',type(xy[0]))
    print('len(xy[0]) = ',len(xy[0]))
    print('l[0] = ',l[0],', b[0] = ',b[0],': x[0] = ',xy[0][0],', y[0] = ',xy[1][0])
    xyTest = ham.lonLatToXY(l[0],b[0])
    print('lonLatToXY(',l[0],',',b[0],') = xyTest.x = ',xyTest.x,', xyTest.y = ',xyTest.y)

    dic[x_key] = [str(a) for a in xy[0]]
    dic[y_key] = [str(a) for a in xy[1]]

    header.append(x_key)
    header.append(y_key)

#    l = lb[:][0]
#    b = lb[:][1]

#    print(''l = ',l
#    print(''b = ',b

    if fname_out is None:
        fname_out = fname_in
    writeDictToCSV(dic, fname_out, header)

def plotGaiaDistApprox(par, ePar, rEst, rLen, doPlot=False):
#    xLo = np.arange(0,float(rEst),1.)
#    xHi = np.arange(float(rEst),float(rEst)*5.,1.)
#    yLo = np.exp(-(xLo-float(rEst))**2 / (2. * (float(rEst)-float(rLo))**2))
#    yHi = np.exp(-(xHi-float(rEst))**2 / (2. * (float(rHi)-float(rEst))**2))
#    plt.plot(xLo,yLo,'b-')
#    plt.plot(xHi,yHi,'r-')
    print('par = ',par)
    print('ePar = ',ePar)
    print('rEst = ',rEst)
#    print('rLo = ',rLo)
#    print('rHi = ',rHi)
    print('rLen = ',rLen)
    r = np.arange(0.00001,5.*float(rEst),1.)
    y = r**2. * np.exp(0. - (r / float(rLen)) - ((((par / 1000.) - (1./r))**2.) / (2. * ((ePar/1000.)**2.))))
    if doPlot:
        plt.plot(r,y)
        plt.show()
    return [r,y]

def calcDistFromGaiaParallax(parallax,eParallax,gLon,gLat,doPlot=False):
    # Input data
    # Specify either l,b or rlen. Set other to NA. rlen takes precedence.
    # parallax    = 1 # parallax in mas (corrected for any zeropoint offset; +0.029mas in the catalogue)
    # eParallax  = abs(0.2*w) # parallax uncertainty in mas
    # glon = 340 # Galactic longitude in degrees (0 to 360)
    # glat =  45 # Galactic latitude (-90 to +90)
    rlen =  "NA" # length scale in pc
    # Plotting parameters in pc
    # rlo,rhi are range for computing normalization of posterior
    # rplotlo, rplothi are plotting range (computed automatically if set to NA)
    rlo = 0
    rhi = 1e5
    rplotlo = "NA"
    rplothi = "NA"

    # Define command and arguments
    command = 'Rscript'
    path2script = '/Users/azuri/entwicklung/r/Gaia-DR2-distances/run_distest_single.R'

    # Variable number of args in a list
    args = [str(parallax),str(eParallax),str(gLon),str(gLat),rlen,str(rlo),str(rhi),rplotlo,rplothi]

    # Build subprocess command
    cmd = [command, path2script] + args

    # Get current working dir
    cwd = os.getcwd()

    # Set current working dir to path2script
    os.chdir(path2script[:path2script.rfind('/')])

    # check_output will run the command and store to result
    x = subprocess.check_output(cmd, universal_newlines=True)

    # Re set current working dir to original
    os.chdir(cwd)

    print('Returned:',type(x),': ',x)
    lines = x.split('\n')
    found = False
    keywords = []
    values = []
    for line in lines:
        if found:
            values = line.split(' ')
            print('dist = ',values[0])
            found = False
        if line.split(' ')[0] == 'rest[pc]':
            found = True
            keywords = line.split(' ')
    result = {}
    for i in range(len(keywords)):
        result[keywords[i]] = values[i]
    print('result = ',result)
    #par,ePar,rEst, rLen
    if doPlot:
        plotGaiaDistApprox(parallax, eParallax, result['rest[pc]'], result['rlen[pc]'])
    return result

def addGaiaDistances(csvFileNameIn,csvFileNameOut):
    if True:
        R.globalenv['inputFileName'] = csvFileNameIn
        R.globalenv['outputFileName'] = csvFileNameOut
        R.r(r'''
            print(inputFileName)
            ''')
        #R.r('sink("/dev/null")')
        # Get current working dir
        cwd = os.getcwd()

        # Set current working dir to path2script
        path2script = '/Users/azuri/entwicklung/gaia_galaxia/r/Gaia-DR2-distances'
        os.chdir(path2script)
        print('current working directory set to <'+os.getcwd()+'>')
        R.r(r'''
            source("functions.R")
            source("./length_scale_model/sphharm_basis.R") # provides sphharm.basis
            print(c("inputFileName = ",inputFileName,", outputFileName = ",outputFileName))

            data <- read.csv(file=inputFileName)
            print(c("data has ",nrow(data)," rows"))
            data <- data[!is.na(data$parallax), ]
            print(c("data has ",nrow(data)," rows"))
            #print(head(data))
            glons <- as.numeric(data$l)
            glats <- as.numeric(data$b)
            ws <- as.numeric(data$parallax)
            wsds <- as.numeric(data$parallax_error)
            rlen <-  NA # length scale in pc
            # Plotting parameters in pc
            # rlo,rhi are range for computing normalization of posterior
            # rplotlo, rplothi are plotting range (computed automatically if set to NA)
            rlo <- 0
            rhi <- 1e5
            rplotlo <- NA
            rplothi <- NA

            data$`rEst[pc]` <- numeric(nrow(data))
            data$`rLo[pc]` <- numeric(nrow(data))
            data$`rHi[pc]` <- numeric(nrow(data))
            data$`rLen[pc]` <- numeric(nrow(data))
            data$result_flag <- integer(nrow(data))
            data$modality_flag <- integer(nrow(data))
            #print(ws)
            for (i in 1:length(ws)) {
              #print(c("i = ",i,", ws[[i]] = ",ws[[i]]))
              if(!is.na(ws[[i]])) {
                w <- ws[[i]]+0.029
                wsd <- wsds[[i]]
                glon <- glons[[i]]
                glat <- glats[[i]]
                rlen <-  NA # length scale in pc
                # Plotting parameters in pc
                # rlo,rhi are range for computing normalization of posterior
                # rplotlo, rplothi are plotting range (computed automatically if set to NA)
                rlo <- 0
                rhi <- 1e5
                rplotlo <- NA
                rplothi <- NA
                res <- getDistFromGaia(w=w, wsd=wsd, glon=glon, glat=glat, calcIfBimod=TRUE)
            #    print(c("res = ",res))
            #    print(c("res$result_flag = ",res$result_flag))
                data$`rEst[pc]`[[i]] <- res[1]#$`rEst[pc]`
                data$`rLo[pc]`[[i]] <- res[2]#$`rLo[pc]`
                data$`rHi[pc]`[[i]] <- res[3]#$`rHi[pc]`
                data$`rLen[pc]`[[i]] <- res[4]#$`rLen[pc]`
                data$result_flag[[i]] <- res[5]#$result_flag
                data$modality_flag[[i]] <- res[6]#$modality_flag
              }
            }
            #print(c("data has ",nrow(data)," rows"))
            data <- data[!is.na(data$`rEst[pc]`), ]
            #print(c("data has ",nrow(data)," rows"))
            write.csv(data,outputFileName, sep=",", row.names = FALSE, quote=FALSE)
        ''')# % (csvFileNameIn,csvFileNameOut)

    # Re set current working dir to original
    os.chdir(cwd)
    if False:
        command = 'Rscript'
        path2script = '/Users/azuri/entwicklung/gaia_galaxia/r/Gaia-DR2-distances/add_distances.R'

        # Variable number of args in a list
        args = [csvFileNameIn,csvFileNameOut]

        # Build subprocess command
        cmd = [command, path2script] + args

        # Get current working dir
        cwd = os.getcwd()

        # Set current working dir to path2script
        os.chdir(path2script[:path2script.rfind('/')])
        print('current working directory set to <'+os.getcwd()+'>')

        # check_output will run the command and store to result
        x = subprocess.check_output(cmd, universal_newlines=True)

        # Re set current working dir to original
        os.chdir(cwd)

        print('Returned:',type(x),': ',x)

    if False:
        csvData = csvFree.readCSVFile(csvFileNameIn)
        rEst = np.zeros(csvData.size())
        rLo = np.zeros(csvData.size())
        rHi = np.zeros(csvData.size())
        rLen = np.zeros(csvData.size())
        result_flag = np.zeros(csvData.size())
        modality_flag = np.zeros(csvData.size())
        toRemove = []
        for i in range(csvData.size()):
            try:
                print('i = ',i,': parallax = ',csvData.getData('parallax',i),', parallax_error = ',csvData.getData('parallax_error',i),', l = ',csvData.getData('l',i),', b = ',csvData.getData('b',i))
                result = calcDistFromGaiaParallax(float(csvData.getData('parallax',i)),
                                                  float(csvData.getData('parallax_error',i)),
                                                  float(csvData.getData('l',i)),
                                                  float(csvData.getData('b',i)))
                rEst[i] = result['rest[pc]']
                rLo[i] = result['rlo[pc]']
                rHi[i] = result['rhi[pc]']
                rLen[i] = result['rlen[pc]']
                result_flag[i] = result['result_flag']
                modality_flag[i] = result['modality_flag']
            except:
                toRemove.append(i)
        csvData.addColumn('rEst[pc]',rEst)
        csvData.addColumn('rLo[pc]',rLo)
        csvData.addColumn('rHi[pc]',rHi)
        csvData.addColumn('rLen[pc]',rLen)
        csvData.addColumn('result_flag',result_flag)
        csvData.addColumn('modality_flag',modality_flag)
        for i in toRemove:
            csvData.removeRow(i)
        csvFree.writeCSVFile(csvData,csvFileNameOut)
