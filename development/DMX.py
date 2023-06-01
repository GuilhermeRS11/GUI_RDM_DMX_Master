
teste = bytes.fromhex(f"{0x24:0{2}X}")

#print test in binary format
def print_binary(test):
    print(''.join(format(x, '08b') for x in test))

def binary_to_hex(binary):
    return int(binary, 2)

print(teste)

print_binary(b'$')