import time
import os
import random
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Progress bar function
def create_progress_bar(percentage, width=50):
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f'[{bar}]'

# Download class
class Download:
    def __init__(self, server_number, total_size):
        self.server_number = server_number
        self.total_size = total_size
        self.downloaded = 0
        self.is_cancelled = False
        self.switch_prompted = False

# File download simulation
def download_file(download, start_time=None):
    if start_time is None:
        start_time = time.time()
    
    while download.downloaded < download.total_size and not download.is_cancelled:
        chunk = random.randint(10, 50)  # Simulate variable chunk sizes
        download.downloaded = min(download.downloaded + chunk, download.total_size)
        progress = (download.downloaded / download.total_size) * 100
        elapsed = time.time() - start_time
        
        progress_bar = create_progress_bar(progress)
        print(f"\rServer {download.server_number}: {progress_bar} {progress:.2f}% | Time: {elapsed:.2f}s", end="")
        
        if download.downloaded >= download.total_size:
            break
        
        time.sleep(0.05)  # Short delay to simulate download time without rate limiting
    
    print()  # New line after download completes
    return False

# ECC encryption function with reused nonce vulnerability
def encrypt_message(public_key, private_key, message, reused_nonce=None):
    shared_key = private_key.exchange(ec.ECDH(), public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"handshake data"
    ).derive(shared_key)

    if reused_nonce:
        nonce = reused_nonce
    else:
        nonce = os.urandom(12)

    aesgcm = AESGCM(derived_key)
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)

    return nonce, ciphertext

# ECC Crypto Challenge function
def ecc_challenge():
    print("\n--- Welcome to the ECC Crypto Challenge! ---")
    
    private_key_sender = ec.generate_private_key(ec.SECP256R1())
    public_key_sender = private_key_sender.public_key()

    private_key_recipient = ec.generate_private_key(ec.SECP256R1())
    public_key_recipient = private_key_recipient.public_key()

    message1 = "picoCTF{ECC_Reused_Nonce_Vulnerability}"
    message2 = "This is another important encrypted message."

    reused_nonce = os.urandom(12)
    nonce1, ciphertext1 = encrypt_message(public_key_recipient, private_key_sender, message1, reused_nonce)
    nonce2, ciphertext2 = encrypt_message(public_key_recipient, private_key_sender, message2, reused_nonce)

    public_key_bytes = public_key_sender.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    challenge_data = f"""ECC Crypto Challenge
Public Key (Sender):
{public_key_bytes.decode()}
Nonce 1: {nonce1.hex()}
Ciphertext 1: {ciphertext1.hex()}
Nonce 2: {nonce2.hex()}
Ciphertext 2: {ciphertext2.hex()}"""

    return challenge_data

# Main function to handle file downloads and challenges
def main():
    total_size = 1000  # Size of the file in KBs

    print("You can download the file from the following Servers:")
    print("1. Server 1 ")
    print("2. Server 2")
    
    choice = input("Enter your choice (1 or 2): ")

    downloads = [
        Download(1, total_size),
        Download(2, total_size)
    ]

    current_server = int(choice) - 1 if choice in ['1', '2'] else 0

    if not download_file(downloads[current_server]):
        print("File downloaded successfully!")
    
    challenge_data = ecc_challenge()
    
    view_choice = input("\nDo you want to view the challenge data? (yes/no): ").lower()
    if view_choice == 'yes':
        print("\n--- Challenge Data ---")
        print(challenge_data)
    
    print("\nAnalyze the challenge data to recover the flag!")
    print("Robin Hood, in his clever quest to outsmart the Sheriff of Nottingham, has provided us with the decrypted second message: 'This is another important encrypted message.'")
    print("Using this information, we can now decrypt the first message, which contains the secret flag.")
    print("Hint: Repetition is the enemy of security.")

if __name__ == "__main__":
    main()
