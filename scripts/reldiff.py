import csv
import argparse

parser = argparse.ArgumentParser(description='Remove values for more efficient plotting.')
parser.add_argument('rt_path', help='path to csv containing rt hdr data')
parser.add_argument('nohz_path', help='path to csv containing ')
args = parser.parse_args()

def linfun(entry, oldentry):
    x1 = float(oldentry[1])
    y1 = float(oldentry[0])
    x2 = float(entry[1])
    y2 = float(entry[0])
    m = (y2-y1)/(x2-x1)
    t = y1-x1*m
    return {'m': m, 't': t}

with open(args.rt_path, newline='') as rtfile:
    with open(args.nohz_path, newline='') as nohzfile:
        rtreader = csv.reader(rtfile, delimiter=';', quotechar='"')
        rtlist = []
        nohzreader = csv.reader(nohzfile, delimiter=';', quotechar='"')
        nohzlist = []
        for rt in rtreader:
            rtlist.append(rt)
        for nohz in nohzreader:
            nohzlist.append(nohz)
        x = 2
        while x < 12000000:
            for e in rtlist:
                if float(e[1]) > x:
                    rtentry = e
                    break
                oldrtentry = e
            for e in nohzlist:
                if float(e[1]) > x:
                    nohzentry = e
                    break
                oldnohzentry = e
            rt_mt = linfun(rtentry, oldrtentry)
            nohz_mt = linfun(nohzentry, oldnohzentry)
            y_rt = rt_mt['m'] * x + rt_mt['t']
            y_nohz = nohz_mt['m'] * x + nohz_mt['t']
            reldiff = y_rt/y_nohz * 100
            print(str(x) + ";" + str(y_rt) + ";" + str(y_nohz) + ";" + str(reldiff))
            x = x * 1.3
