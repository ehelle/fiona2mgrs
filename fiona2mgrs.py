import mgrs
import fiona
import sys, getopt

myfile = ("./setermoen.json")

def printMGRS(coords):
    if isinstance(coords, list):
        print("[")
        for elt in coords:
            printMGRS(elt)
        print("]")
    elif isinstance(coords, tuple):
        print(lonlat2mgrs(coords[0], coords[1]))
    else:
        return

def lonlat2mgrs(lon, lat):
    return mgrs.MGRS().toMGRS(lat, lon)

def fiona2mgrs(infile, outfile):
    with open(outfile, 'w') as out:
        original_stdout = sys.stdout
        sys.stdout = out
        with fiona.open(infile) as src:
            for f in src:
                printMGRS(f['geometry']['coordinates'])
        sys.stdout = original_stdout

def main(argv):
    infile=""
    outfile=""
    help_string = 'finona2mgrs -i <inputfile> -o <outputfil>'
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
        elif opt == '-i':
            infile = arg
        elif opt =='-o':
            outfile = arg
    if infile == "" or outfile == "":
        print(help_string)
        sys.exit(2)
    fiona2mgrs(infile, outfile)

if __name__ == '__main__':
    main(sys.argv[1:])
