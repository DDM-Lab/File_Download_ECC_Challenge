def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Given data
ciphertext1 = bytes.fromhex("d7dcea30eac2bacf0c320a9f6830520afcfcceabe4a3600d7b0dfcc4da1375c9fb8676f748453df6cd5d5b446e763f14f5961300")
ciphertext2 = bytes.fromhex("c5d8e224b1ee8aac320e009e73304475d7fdc3baf88c421d7343f4d3c8027dc2f7dcce7cc480b3dde0b95adac5322aa66827")
known_message2 = "This is another encrypted message.".encode()

# XOR the two ciphertexts to get the XOR of the plaintexts
xor_plaintexts = xor_bytes(ciphertext1, ciphertext2)

# Recover the first message by XORing the known second message with the XOR of the plaintexts
recovered_message1 = xor_bytes(known_message2, xor_plaintexts)

# Output the results
print("Flag:", recovered_message1.decode())