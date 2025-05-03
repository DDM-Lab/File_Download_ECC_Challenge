# Reused noncense

- Namespace: picoctf/research
- ID: file-download-ecc-control
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: no
- MaxUsers: 1

## Description

Let's analyze insecure ECC cryptography and find out why reused nonces are bad.
Can you write a Python script that uses the ciphertexts and plaintext to recover the flag?

**NOTE: Do not close the Qualtrics survey.**

## Details
Connect to the program with netcat:

`$ nc {{server}} {{port}}`

**NOTE: Do not forget to save the Qualtrics data along with the flag!**

## Hints

- Start by converting the hex-encoded ciphertext and known-plaintext into bytes.
- XOR the known-plaintext bytes with the second ciphertext (the known-plaintext one).
- Use the result of the XOR to decrypt the first ciphertext.
- You can use the walkthrough provided in the Qualtrics survey.

## Solution Overview

XOR the two provided cipher texts, then XOR with the known plain text to get the flag.

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
pidslimit: 20
ulimits:
  - nofile=128:128
diskquota: 64m
init: true
```

## Learning Objective

Understand why reused nonces are vulnerable.

## Attributes

- author: DDM LAB
- organization: picoCTF
- event: picoCTF Experimental Problems 2
