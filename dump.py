import os
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("soundtable")
args = parser.parse_args()

f0 = open(args.soundtable, "rb")
f0.seek(0x00, os.SEEK_END)
f0.seek(-0x04, os.SEEK_CUR)
footer = struct.unpack('I', f0.read(4))[0]

if footer != 0x00C0FFEE:
    raise ValueError("Not an SLB!")

f1 = open(args.soundtable[:-4] + ".txt", 'w')
print("Dumping SoundTable...")
f0.seek(0x00, os.SEEK_SET)
amount = struct.unpack('I', f0.read(4))[0]
f0.seek(0x04, os.SEEK_CUR)

for i in range(0, amount):
    pointer = struct.unpack('I', f0.read(4))[0]
    getBack = f0.tell()
    f0.seek(pointer, os.SEEK_SET)
    length = struct.unpack('B', f0.read(1))[0]
    name = f0.read(length).decode()
    print("Name: " + name)
    f1.write(name)
    f1.write(',')
    f0.seek(getBack, os.SEEK_SET)
    variety = struct.unpack('I', f0.read(4))[0]
    print("Variety: " + str(variety))
    f1.write(str(variety))
    f1.write(',')
    volume = struct.unpack('f', f0.read(4))[0]
    print("Volume: " + str(volume))
    f1.write(str(volume))
    f1.write("\n")

print("Done!")
f0.close()
f1.close()
