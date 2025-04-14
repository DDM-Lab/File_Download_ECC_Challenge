# Sanity Download

- Namespace: picoctf/research
- ID: file-download-ecc
- Type: custom
- Category: Cryptography
- Points: 1
- Templatable: no
- Max Users: 1

## Description
Simulate file downloads and analyze insecure ECC cryptography 

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
## Attributes

- author: DDM Lab
- organization: picoCTF
- event: S-25 ddmlab reseach study
