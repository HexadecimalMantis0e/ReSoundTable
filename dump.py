import os
import struct
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("SoundTable")
args = parser.parse_args()

f0 = open(args.SoundTable,"rb")
f1 = open("out.txt","w")

f0.seek(0x00, os.SEEK_END)
f0.seek(-0x04, os.SEEK_CUR)
footer = struct.unpack('i', f0.read(4))[0]

if footer != 0x0C0FFEE:
    raise ValueError("Not an SLB")

f0.seek(0x00, os.SEEK_SET)

amount = struct.unpack('i', f0.read(4))[0]

f0.seek(0x04, os.SEEK_CUR)


for i in range(0,amount):

    pointer = struct.unpack('i', f0.read(4))[0]

    getBack = f0.tell()

    f0.seek(pointer,os.SEEK_SET)

    length = struct.unpack('B', f0.read(1))[0]

    name = f0.read(length)
    print "Name: " + name

    f1.write(name)
    f1.write(",")

    f0.seek(getBack,os.SEEK_SET)

    variety = struct.unpack('i', f0.read(4))[0]
    print "Variety: " + str(variety)

    floatValue = struct.unpack('f', f0.read(4))[0]
    print "Volume: " + str(floatValue)

    f1.write(str(variety))
    f1.write(",")
    f1.write(str('%.5s' % ('%.4f' % floatValue)))
    f1.write("\n")
