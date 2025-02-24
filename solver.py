def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Given data
ciphertext1 = bytes.fromhex("ba65f2f05059fb1a29401fafc1055eef4609eb7927fce4fb0efc9aa358853cbe101f0fbcfa5f09f341ed195163a6f02239b28ccb7d0036")
ciphertext2 = bytes.fromhex("9e64f8ec3364ce410d6d3384fb0559bc4a00c4583ae6e6f0258a8aa1559237af061307f5e3430767b638fa29ac9eed543ad64d1c27779a1ef073b361")
known_message2 = "This is another important encrypted message".encode()

# XOR the two ciphertexts to get the XOR of the plaintexts
xor_plaintexts = xor_bytes(ciphertext1, ciphertext2[:len(ciphertext1)])

# Recover the first message by XORing the known second message with the XOR of the plaintexts
recovered_message1 = xor_bytes(known_message2[:len(xor_plaintexts)], xor_plaintexts)

# Output the results
print("Recovered message (hex):", recovered_message1.hex())
print("Recovered message (ascii):", ''.join(chr(b) if 32 <= b <= 126 else '.' for b in recovered_message1))
