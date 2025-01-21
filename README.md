# sunk-cost

#  ECC Crypto Challenge

This project simulates a secure file download which includes an Elliptic Curve Cryptography (ECC) challenge. It demonstrates variable download rates, user interaction, and a cryptographic vulnerability using ECC with reused nonces.



## Requirements

- Python 3.6 or above
- cryptography library

## Installation

1. Clone this repository or download the script.
   
``` git clone https://github.com/saketh7502/Sunk_Cost_DDMLab.git ```

3. Install the required library:
```
pip install cryptography
```


## Usage

Run the script using Python:
```
python sunkcost.py
```


Follow the on-screen prompts to:
1. Choose a server for file download
2. Optionally switch servers during download
3. View the ECC crypto challenge data

## File Download Simulation

The script simulates downloading a file from two servers:
- Server 1: Constant download rate
- Server 2: Variable download rate (decreases over time)

Users can switch servers during the download process.

## ECC Crypto Challenge

After the file download, an ECC encryption challenge is presented. This challenge demonstrates a vulnerability when reusing nonces in ECC encryption.

### Challenge Components:
- Sender's public key
- Two encrypted messages using the same nonce
- Nonces used for encryption

Thoughs:

- Provide a better explanation of what the user is downloading and why. For example: 
> "Download the encrypted files from the server of your choice to begin the challenge."
- At the beginning, inform users that they can switch servers at any time but warn them about the potential consequences  b:
> Message: "You can switch servers at any point during the download, but doing so will reset your progress. Choose wisely!"
- Before switching, ask for confirmation (suggestion):
> Message: "Switching servers will reset your download progress. Are you sure you want to switch? (yes/no)"
- At the end, we should have the time they took when the throttling began and if they switched:

```Download Analysis:
- Total Download Time: 45 seconds
- Number of Server Switches: 0
- Throttling began at: 80%```
