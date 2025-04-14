def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Given data
ciphertext1 = bytes.fromhex("07105cb4549a2d5c726eb4282f492a0607f9ee1541b70af667b501472d4ca48500f9a93e5ab38f624f4d6965155b41cd86f74ea5bf7095")
ciphertext2 = bytes.fromhex("231156a837a718075643980315492d550bf0c13403ad08fd4cc31145205baf9416f5a17743af81824e79c218767ee04e6c990738b5b4ac1306bf8e")
known_message2 = "This is another important encrypted message".encode()

# XOR the two ciphertexts to get the XOR of the plaintexts
xor_plaintexts = xor_bytes(ciphertext1, ciphertext2[:len(ciphertext1)])

# Recover the first message by XORing the known second message with the XOR of the plaintexts
recovered_message1 = xor_bytes(known_message2[:len(xor_plaintexts)], xor_plaintexts)

# Output the results
print("Recovered message (hex):", recovered_message1.hex())
print("Recovered message (ascii):", ''.join(chr(b) if 32 <= b <= 126 else '.' for b in recovered_message1))
