import astroutils as utils

whichOne = 'SDSS'

if whichOne == 'simbad':
    fname = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/csvs.list'
    csvs = None
    with open(fname) as f:
        csvs = f.readlines()
    csvs = [fname[0:fname.rfind('/')+1]+l.rstrip() for l in csvs]
    header = utils.readCSVHeader(csvs[0])
    i = 0
    for fname in csvs:
        print('running file <'+fname+'>')
        if i > 0:
            utils.addHeader(fname, header)
        utils.add_lb_to_csv_file(fname, 'ra_epoch2000', 'dec_epoch2000')#, fname_out = fname+'.new')
        i += 1
elif whichOne == 'SDSS':
    fname = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2distXSDSS12/GaiaXSDSS_mean.csv'
    fname_lb = fname[:fname.rfind('.')]+'_lb.csv'
#    utils.add_lb_to_csv_file(fname, 'RA_ICRS', 'DE_ICRS', fname_out = fname_lb)
    fname_xy = fname_lb[:fname_lb.rfind('.')]+'_xy.csv'
    utils.add_xy_to_csv_file(fname_lb, 'l', 'b', 'hammerX', 'hammerY', fname_out = fname_xy)
