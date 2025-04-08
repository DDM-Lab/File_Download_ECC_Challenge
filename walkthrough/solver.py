def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Given data
ciphertext1 = bytes.fromhex("FIXME")
ciphertext2 = bytes.fromhex("FIXME")
known_message2 = "FIXME".encode()

# XOR the two ciphertexts to get the XOR of the plaintexts
xor_plaintexts = xor_bytes(FIXME, ciphertext2[:len(ciphertext1)])

# Recover the first message by XORing the known second message with the XOR of the plaintexts
recovered_message1 = xor_bytes(known_message2[:len(xor_plaintexts)], xor_plaintexts)

# Output the results
print("Recovered message (hex):", recovered_message1.hex())
print("Recovered message (ascii):", ''.join(chr(b) if 32 <= b <= 126 else '.' for b in recovered_message1))
