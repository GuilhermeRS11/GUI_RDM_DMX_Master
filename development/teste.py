# Set a list and print it

a = [0x08, 0x64]

# turn the list into a 16bit hex
b = (a[0] << 8) | a[1]

print(b)