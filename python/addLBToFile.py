import astroutils as utils

fname = '/Volumes/obiwan/azuri/data/gaia/x-match/GaiaDR2xSimbad/csvs.list'
csvs = None
with open(fname) as f:
    csvs = f.readlines()
csvs = [fname[0:fname.rfind('/')+1]+l.rstrip() for l in csvs]
header = utils.readCSVHeader(csvs[0])
i = 0
for fname in csvs:
    print 'running file <'+fname+'>'
    if i > 0:
        utils.addHeader(fname, header)
    utils.add_lb_to_csv_file(fname, 'ra_epoch2000', 'dec_epoch2000')#, fname_out = fname+'.new')
    i += 1