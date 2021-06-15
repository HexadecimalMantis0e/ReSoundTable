import os
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("text")
args = parser.parse_args()

groups = []
f0 = open(args.text, 'r')
f1 = open(args.text[:-4] + ".slb", "wb")

print("Creating SoundTable...")
line = f0.readline()

while line:
    editedLine = line.strip()
    groupData = editedLine.split(',')
    groups += [groupData]
    line = f0.readline()

groupCount = len(groups)
f1.write(struct.pack('I', groupCount))
f1.write(struct.pack('I', 0x08))
pointer = groupCount * 0x0C + 0x08

for i in range(0, groupCount):
    f1.write(struct.pack('I', pointer))
    print("Pointer: " + hex(pointer))
    getBack = f1.tell()
    f1.seek(pointer, os.SEEK_SET)
    length = len(groups[i][0])
    f1.write(struct.pack('B', length))
    f1.write(groups[i][0].encode())
    print("Name: " + groups[i][0])
    f1.write(struct.pack('B', 0x00))
    f1.seek(getBack, os.SEEK_SET)
    f1.write(struct.pack('I', int(groups[i][1])))
    print("Variety: " + groups[i][1])
    f1.write(struct.pack('f', float(groups[i][2])))
    print("Volume: " + groups[i][2])
    pointer += length + 0x02

f1.seek(pointer, os.SEEK_SET)
totalBytes = pointer

# Handle padding
while totalBytes % 0x04 != 0x00:
    f1.write(struct.pack('B', 0x00))
    totalBytes += 0x01

f1.write(struct.pack('I', 0x04))
pointer = 0x08

for i in range(0, groupCount):
    f1.write(struct.pack('I', pointer))
    print("Pointer: " + hex(pointer))
    pointer += 0x0C

f1.write(struct.pack('I', groupCount + 0x01))
f1.write(struct.pack('I', 0x00C0FFEE))
print("Done!")
f0.close()
f1.close()
