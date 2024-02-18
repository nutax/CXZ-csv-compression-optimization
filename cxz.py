import lzma
import pickle
import sys
import time

def main():
    procedure, input_file, output_file = read_args()
    procedures = {"c": compress,"d": decompress}
    procedures[procedure](input_file, output_file)

def read_args():
    if len(sys.argv) != 4:
        print("python3 cxz.py [c | d] [input file] [output file]")
        sys.exit(1)
        
    _, procedure, input_file, output_file = sys.argv
    return procedure, input_file, output_file

def compress(input_file, output_file):
    print("compressing")
    start = time.time()
    with open(input_file, "r") as file:
        data = file.read().strip().split('\n')
    header, data = data[0], data[1:]
    data = [[val for val in row.strip().split(',')] for row in data]
    data = transpose(data)
    data = [','.join(col).encode('utf-8') for col in data]
    data = [lzma.compress(col, format=lzma.FORMAT_XZ, preset=3) for col in data]
    with open(output_file, "wb") as file:
        pickle.dump({"h":header, "d": data}, file)
    print("Elapsed:", time.time()-start, "seconds")

def decompress(input_file, output_file):
    print("decompressing")
    start = time.time()
    with open(input_file, "rb") as file:
        data = pickle.load(file)
    header, data = data["h"], data["d"]
    data = [lzma.decompress(col, format=lzma.FORMAT_XZ).decode('utf-8') for col in data]
    data = [[val for val in col.strip().split(',')] for col in data]
    data = transpose(data)
    data = [','.join(row) for row in data]
    print(data[0])
    data = [header] + data
    data = '\n'.join(data)
    with open(output_file, "w") as file:
        file.write(data)
    print("Elapsed:", time.time()-start, "seconds")

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

main()
