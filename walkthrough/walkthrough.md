# CTF Challenge: Download

## Overview

This challenge simulates a real-world cryptographic vulnerability involving nonce reuse in stream ciphers. Your goal is to recover a hidden flag by exploiting a critical cryptographic vulnerability.

In this walkthrough you have two files:
1. This file `walkthrough.md`
2. The solver `solver.py`

## The Vulnerability: Nonce Reuse in Stream Ciphers

In this challenge, an encryption system using AES-GCM (a stream cipher mode) commits a critical security error: **reusing the same nonce for multiple encryptions**. 

When a nonce (number used once) is reused in stream ciphers:

1. The same keystream is generated for both encryptions
2. This allows an attacker to XOR the two ciphertexts together
3. The result is equivalent to the XOR of the two plaintexts
4. If one plaintext is known, the other can be recovered!

This vulnerability is sometimes called a "two-time pad" attack or "stream cipher key reuse" attack.

## Step-by-Step Solution Guide

### 1. Run the Challenge

You can change download servers if you want, by clicking CTRL+C but you lose your progress.

After the download, you'll receive cryptographic challenge data, including:
- A public key
- Two nonces (which are identical)
- Two ciphertexts
- The decrypted plaintext of the second ciphertext: "This is another important encrypted message."


### 2. Complete the Solver Script

Open `solver.py` and follow these steps to complete it:

1. **Replace the FIXME placeholders** with the actual hex values from the challenge output:
   - `ciphertext1` - Replace with the hex value of "Ciphertext 1"
   - `ciphertext2` - Replace with the hex value of "Ciphertext 2"
   - `known_message2` - Replace with `"This is another important encrypted message"`

2. **Complete the XOR calculation**:
   - Replace the FIXME in `xor_plaintexts = xor_bytes(FIXME, ciphertext2[:len(ciphertext1)])` with `ciphertext1`

3. Save your changes to `solver.py`

### 3. Run the Solver

Execute your completed solver script:

```bash
python solver.py
```

### 4: Submitting Your Result

If you've done everything correctly, you should see the recovered message containing the flag.

1. Create a file named `download_challenge.txt` and copy/paste the Qualtrics information into this file.
2. Upload `download_challenge.txt` to Qualtrics to receive credit for completing the challenge.
3. Submit the flag to Qualtrics.

## How the Attack Works

Let's break down the mathematics behind this attack:

1. In a stream cipher, encryption works by: `ciphertext = plaintext ⊕ keystream`
   (where ⊕ represents the XOR operation)

2. When the same nonce is reused, both encryptions use the same keystream:
   - `ciphertext1 = plaintext1 ⊕ keystream`
   - `ciphertext2 = plaintext2 ⊕ keystream`

3. XORing the two ciphertexts:
   - `ciphertext1 ⊕ ciphertext2 = (plaintext1 ⊕ keystream) ⊕ (plaintext2 ⊕ keystream)`

4. The keystream cancels out due to XOR properties:
   - `ciphertext1 ⊕ ciphertext2 = plaintext1 ⊕ plaintext2`

5. Since we know `plaintext2`, we can recover `plaintext1`:
   - `(ciphertext1 ⊕ ciphertext2) ⊕ plaintext2 = plaintext1 ⊕ plaintext2 ⊕ plaintext2 = plaintext1`

### Understanding XOR Properties

The XOR operation has these important properties that make this attack possible:

- **Commutativity**: A ⊕ B = B ⊕ A
- **Associativity**: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
- **Identity**: A ⊕ 0 = A
- **Self-inverse**: A ⊕ A = 0

The last property is especially important for this attack - it means any value XORed with itself cancels out to zero, which is how we remove the keystream and the known plaintext from our equations.

## Learning Objectives

After completing this challenge, you should understand:

1. Why nonces/IVs must never be reused in stream ciphers
2. How XOR mathematics can be used to attack crypto implementations
3. The importance of proper cryptographic key management
4. How to implement a practical crypto attack in Python
5. The real-world implications of cryptographic vulnerabilities

## Security Best Practices

To avoid this vulnerability in real systems:

1. **Never reuse nonces** - Use a secure method to generate unique nonces for each encryption
2. **Use authenticated encryption** - AES-GCM actually includes authentication, but misuse can still be catastrophic
3. **Consider nonce-misuse resistant algorithms** - Some algorithms like AES-GCM-SIV are designed to be more resistant to nonce reuse
4. **Implement proper key rotation** - Regularly changing encryption keys limits the impact of cryptographic mistakes

## Additional Resources

To deepen your understanding of these concepts:

1. [Stream Cipher Reused Key Attack](https://en.wikipedia.org/wiki/Stream_cipher_attacks#Reused_key_attack) - Wikipedia article on stream cipher attacks
2. [The Dangers of AES-GCM Nonce Reuse](https://soatok.blog/2020/05/13/why-aes-gcm-sucks/) - Blog post explaining AES-GCM security issues
3. [XOR Properties in Cryptography](https://crypto.stackexchange.com/questions/59/taking-advantage-of-one-time-pad-key-reuse) - Stack Exchange post on XOR math
4. [NIST Guidelines on Cryptographic Key Management](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf) - Official security recommendations
5. [Cryptopals Crypto Challenges](https://cryptopals.com/) - An excellent set of practical cryptography challenges, including similar attacks

## Troubleshooting

If you're having trouble with the solution:
- Double-check that you've correctly copied all hex values from the challenge output
- Ensure you're using the exact known plaintext as provided

Remember: In a real-world scenario, this type of vulnerability could lead to complete compromise of an encryption system. Many high-profile cryptographic failures have occurred due to nonce reuse!