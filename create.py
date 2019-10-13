import os
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("Text")
args = parser.parse_args()


newarr = []
f0 = open(args.Text,"rb")

f2 = open("out.slb","wb")
totalstringsbytes = 0x04
strgroupcount = 0x00
line = f0.readline()
while line:
    #print line.strip()
    new = line.strip()
    new2 = new.split(",")
    #print new2
    newarr += [new2]
    strgroupcount += 0x01
    totalstringsbytes += 0x0c

    line = f0.readline()

pointer = strgroupcount * 0x0c + 0x8

f2.write(struct.pack("i", strgroupcount))
f2.write(struct.pack("i", 0x08))

for i in range(0,strgroupcount):
    f2.write(struct.pack("i", pointer))
    getBack = f2.tell()
    print "Pointer: " + hex(pointer)
    f2.seek(pointer, os.SEEK_SET)
    get = len(newarr[i][0])
    f2.write(bytearray([get]))
    f2.write(newarr[i][0])
    f2.write(bytearray([0]))
    f2.seek(getBack, os.SEEK_SET)
    f2.write(struct.pack("i", int(newarr[i][1])))
    f2.write(struct.pack("f", float(newarr[i][2])))
    totalstringsbytes += get + 0x02
    pointer += 0x02 + get

f2.seek(pointer, os.SEEK_SET)

# Handle padding

while totalstringsbytes % 0x04 != 0x00:
    f2.write(bytearray([0]))
    totalstringsbytes += 0x01

pointer = 0x08
f2.write(struct.pack("i", 0x04))

for i in range(0,strgroupcount):
    f2.write(struct.pack("i", pointer))
    pointer+=0x0c

f2.write(struct.pack("i", strgroupcount + 0x01))
f2.write(struct.pack("i", 0xC0FFEE))
