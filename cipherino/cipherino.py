import random
import argparse

def shuffle_cipher(source, password):
    random.seed(password)
    length = len(source)

    print("Start ciphering");
    for i in range(length):
        shift = random.randint(i, length - 1)
        temp = source[i]
        source[i] = source[shift]
        source[shift] = temp

    print("Done ciphering")
   
def shuffle_decipher(source, password):
    print("Start deciphering")
    random.seed(password)
    length = len(source)
    shifts = []

    print("Generating shifts")
    shifts = [random.randint(i, length - 1) for i in range(length)]

    print("Start deciphering")
    for i in range(length - 1, -1, -1):
        temp = source[i]
        source[i] = source[shifts[i]]
        source[shifts[i]] = temp

    print("Done deciphering")

def get_bytes(path):
    with open(path, "rb") as binary_file:
        data = bytearray(binary_file.read())
    return data

def write_bytes(path, data):
    with open(path, "wb") as binary_file:
        binary_file.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="Password")
    parser.add_argument("-i", help="Input file")
    parser.add_argument("-o", help="Output file")
    parser.add_argument("-m", help="Mode: d[ecipher] or c[ipher]", choices=["d", "c"])
    args = parser.parse_args()

    data = get_bytes(args.i)
    
    if args.m == "c":
        shuffle_cipher(data, args.p)
    if args.m == "d":
        shuffle_decipher(data, args.p)

    write_bytes(args.o, data)
