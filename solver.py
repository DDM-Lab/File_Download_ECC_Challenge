def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Given data
ciphertext1 = bytes.fromhex("784b04960cf5989be1bf37835a7ffc9dd86ac0c7315ddaf9815b8539bf29b7a483ea2dead2052620d599e2b142edde3b9128b5ad4be4db")
ciphertext2 = bytes.fromhex("5c4a0e8a6fc8adc0c5921ba8607ffbced463efe67247d8f2aa2d953bb23ebcb595e625a3cb192821b91c72d93555703a55622b17c2e1baa872dc98")
known_message2 = "This is another important encrypted message".encode()

# XOR the two ciphertexts to get the XOR of the plaintexts
xor_plaintexts = xor_bytes(ciphertext1, ciphertext2[:len(ciphertext1)])

# Recover the first message by XORing the known second message with the XOR of the plaintexts
recovered_message1 = xor_bytes(known_message2[:len(xor_plaintexts)], xor_plaintexts)

# Output the results
print("Recovered message (hex):", recovered_message1.hex())
print("Recovered message (ascii):", ''.join(chr(b) if 32 <= b <= 126 else '.' for b in recovered_message1))
