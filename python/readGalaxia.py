import ebf
import gxutil
import numpy

fileToRead = '/Volumes/yoda/azuri/data/galaxia/sdss/galaxia_185_55.ebf'

def iterAll(filename, cache):
    tagname = '/'
    ckon=1
    recon=0

    begin=0
    end=cache

    path = tagname.strip()
    mydict = {}
    x = ''
    rows=-1

    location=ebf._EbfMap.get(filename, path.lower(),ckon)
    node=ebf._EbfUtils.searchPathTree(_EbfMap.ltable[filename]['pathtree'],path.lower())

    if (node['name'] == path.lower()):
        while begin < header.dim[0]:
            if len(node['files']) > 0:
                for key in node['files']:
                    if rows > -1:
                        temp=ebf.getHeader(filename,node['name']+key).getshape()
                        if len(temp) == 0:
                            temp=numpy.array([1],dtype='int64')
                        if temp[0] == rows:
                            mydict[key] = read(filename,node['name']+key,recon,0,begin,end)
                    else:
                        mydict[key] = read(filename,node['name']+key,recon,0)
            if (recon > 0)&(len(node['dirs']) > 0):
                if recon == 2:
                    for key in node['dirs'].keys():
                        mydict[key.strip('/')] = read(filename,node['name']+key,recon,0)
                if recon == 1:
                    for key in node['dirs'].keys():
                        if (key.startswith('.ebf/') == False)and(key.startswith('.tr/') == False):
                            mydict[key.strip('/')] = read(filename,node['name']+key,recon,0)

            yield mydict
            begin=end
            end =end+cache
            if end > header.dim[0]:
                end=header.dim[0]

# print statistics
#ebf.info(fileToRead)

"""read all parameters in iterations - not tested"""
#iIter = 0
#it = iterAll(fileToRead, 100000)
#print 'it_px = ',type(it),': ',it
#for data in it:
#    print 'type(data) = ',type(data)
#    print 'dir(data) = ',dir(data)
#
#    for key in data.keys():
#        print 'iIter = ',iIter,': data[',key,'] = ',type(data[key]),': ',data[key]
#        print 'iIter = ',iIter,': data[',key,'] = ',len(data[key]),': ',type(data[key]),', type(data[',key,'][0]) = ',type(data[key][0]),', data[',key,'] = ',data[key]
#    iIter += 1

"""read one parameter + all other parameters with the same size in iterations"""
iIter = 0
cache = 100

data = ebf.iterate(fileToRead, '/px+', cache)
print 'data = ',type(data),': ',data

for it in data:
    print 'it = ',type(it),': ',it
    print 'dir(it) = ',dir(it)
    print 'it.keys() = ',it.keys()

    keys = it.keys()
    for key in keys:
        print 'key = ',key
        print 'it[',key,'] = ',len(it[key]),': ',it[key]
        print 'it[',key,'][0] = ',it[key][0]
    l, b, r = gxutil.xyz2lbr(it['px'],it['py'], it['pz'])
    print 'l = ',l,', b = ',b,', r = ',r
    STOP

"""read one parameter in iterations"""
#iIter = 0
#it_px = ebf.iterate(fileToRead, '/px', 100000)
#print 'it_px = ',type(it_px),': ',it_px
#for data in it_px:
#    print 'iIter = ',iIter,': data = ',type(data),': ',data
#    print 'iIter = ',iIter,': data = ',len(data),': ',type(data),', type(data[0]) = ',type(data[0]),', data = ',data
#    iIter += 1

"""read all data - not enough memory for large files"""
#data = ebf.read(fileToRead, '/')
#print 'data = ',type(data),': ',data
#print 'data["px"] = ',len(data["px"]),': ',type(data["px"]),', type(data["px"][0]) = ',type(data["px"][0]),', data["px"] = ',data["px"]
