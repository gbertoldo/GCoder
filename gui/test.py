
def readFile(filename):
    path = []
    try:
        with open(filename) as ifile:
            for line in ifile.readlines():
                sline = line.split(" ")
                path.append([float(sline[0]),float(sline[1])])
    except:
        path = None

    return path

path = readFile("/home/guilherme/ownCloud/CNC/GCoder/gui/test.txt")

if path:
    for p in path:
        print(p)
else:
    print("Error")
