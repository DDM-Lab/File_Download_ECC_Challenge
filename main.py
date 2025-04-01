import time
import os
import argparse
import signal
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import random


# Default condition settings
treatment_mode = True  # Default to control condition
debug_mode = False


# Global variable to handle CTRL+C
interrupt_received = False
already_switched = False
server_start_time = None
# Progress bar function
def create_progress_bar(percentage, width=50):
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f'[{bar}]'

# Download class
class Download:
    def __init__(self, server_number, total_size, download_rate, throttle_point=None):
        self.server_number = server_number
        self.total_size = total_size
        self.download_rate = download_rate
        self.throttle_point = throttle_point
        self.downloaded = 0
        self.is_cancelled = False
        self.is_throttled = False

# Signal handler for CTRL+C
def signal_handler(signum, frame):
    global interrupt_received, already_switched, server_start_time
    
    if already_switched:
        print("\n\033[93mYou have already switched servers once. You must continue with this server.\033[0m")
        return
        
    interrupt_received = True
    server_start_time = time.time()
    print("\n\033[93mInterrupt received. Preparing to switch servers...\033[0m")

# File download simulation
def download_file(download, start_time=None):
    global interrupt_received
    global server_start_time
    if start_time is None:
        start_time = time.time()
        
    if server_start_time is None:
        server_start_time = time.time()
    throttle_percentage = None
    while download.downloaded < download.total_size and not download.is_cancelled and not interrupt_received:
        current_rate = download.download_rate
        
        # Progressive throttling for treatment condition (only for Server 1)
        if download.throttle_point and (download.downloaded / download.total_size) >= download.throttle_point:
            if not download.is_throttled:
                download.is_throttled = True
                # No notification about throttling
            
            # Calculate how far past the throttle point we are (0 to 1 scale)
            progress_past_throttle = (download.downloaded / download.total_size - download.throttle_point) / (1 - download.throttle_point)
            
            # Start at 50% throttle and increase up to 90% throttle
            throttle_factor = 0.6 * (0.01 ** progress_past_throttle)  
            throttle_factor = max(0.05, throttle_factor)  # Ensure we don't go below 10% of original speed
            
            current_rate = current_rate * throttle_factor
        
        chunk = min(current_rate, download.total_size - download.downloaded)
        download.downloaded += chunk
        progress = (download.downloaded / download.total_size) * 100
        elapsed = time.time() - server_start_time
        # elapsed = time.time() - start_time
        
        progress_bar = create_progress_bar(progress)
        
        # Simple status line with no throttling indicator
        status = f"\r\033[1mServer {download.server_number}:\033[0m {progress_bar} \033[92m{progress:.2f}%\033[0m | Speed: \033[94m{current_rate:.2f} KB/s\033[0m | Time: \033[95m{elapsed:.2f}s\033[0m"
        
        print(status, end="", flush=True)
        
        time.sleep(1)
    
    # Calculate final progress percentage and elapsed time
    final_progress = (download.downloaded / download.total_size) * 100
    
    
    if download.is_cancelled or interrupt_received:
        print(f"\n\033[91mServer {download.server_number} download cancelled.\033[0m")
    
    # Return tuple: (success, elapsed_time, final_progress, throttle_percentage)
    return (
        not (download.is_cancelled or interrupt_received),
        elapsed,
        final_progress,
        throttle_percentage
    )


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
    print("\n\033[1m--- Welcome to the ECC Crypto Challenge! ---\033[0m")
    
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
def main(is_treatment, debug):
    global interrupt_received
    total_size = 1000  # Size of the file in KBs

    # Set download rates based on condition
    if is_treatment:
        server1_rate = 30  # Server 1 speed in KB/s for treatment
        server2_rate = 30  # Server 2 speed in KB/s for treatment
    else:
        server1_rate = 30  
        server2_rate = 30

    if debug:
        condition = "Treatment" if is_treatment else "Control"
        print(f"\033[94m[DEBUG MODE] Running in {condition} condition.\033[0m")

    print("\033[1mYou can download the file from the following Servers:\033[0m")
    print(f"\033[94m1. Server 1 \033[0m")
    print(f"\033[94m2. Server 2 \033[0m")

    choice = input("\033[1mEnter your choice (1 or 2): \033[0m")
    initial_server_choice = int(choice)  # Record initial choice

    # For treatment condition, set throttle point to 60% (only for Server 1)
    throttle_point = None
    if is_treatment:
        throttle_points = [0.3,0.4,0.5,0.6,0.7]
        throttle_point = random.choice(throttle_points)
        if choice == '1' and debug:
            print(f"\033[93m[DEBUG MODE] Treatment condition: First server selected will experience throttling at {throttle_point:.0%} progress\033[0m")
        elif debug:
            print(f"\033[93m[DEBUG MODE] Treatment condition: First server selected (Server {initial_server_choice}) will experience throttling at {throttle_point:.0%} progress\033[0m")
    
    current_server = int(choice) - 1 if choice in ['1', '2'] else 0
    other_server = 1 - current_server
    downloads = [
        Download(1, total_size, server1_rate, throttle_point if current_server == 0 else None),
        Download(2, total_size, server2_rate, throttle_point if current_server == 1 else None)
    ]


    print(f"\n\033[1mStarting download from Server {current_server + 1}...\033[0m")
    print("\033[91mPress CTRL+C to switch servers at any time. But progress will be lost.\033[0m")

    # Set up the signal handler for CTRL+C
    signal.signal(signal.SIGINT, signal_handler)


    # --- Data Collection Variables ---
    global already_switched  # Reference the global variable
    already_switched = False  # Reset at the start of each run
    overall_start_time = time.time()
    switch_count = 0
    server_history = [current_server + 1]  # Record initial server
    server_times = [0, 0]  # Time spent in each server (index 0 = Server 1, index 1 = Server 2)
    server_progress = [0, 0]  # Final progress in each server
    switch_percentage = None  # Percentage at which the user switched
    throttle_percentage = None  # Percentage at which throttling began
    download_completed = False
    server_start_time = time.time()
    while True:
        interrupt_received = False
        result = download_file(downloads[current_server], server_start_time)  # Pass start_time
        success, elapsed_time, final_progress, throttle_pct = result
        
        server_progress[current_server] = final_progress
        # Record throttle percentage if it occurred
        if throttle_pct is not None:
            throttle_percentage = throttle_pct
        if success:
            print("\n\033[92mFile downloaded successfully!\033[0m")
            download_completed = True
            server_times[current_server] = elapsed_time
            break
        else:
            if not already_switched:
                print("\n\033[93mSwitching to the other Server...\033[0m")
                server_times[current_server] = elapsed_time
                switch_percentage = final_progress
                switch_count += 1
                current_server, other_server = other_server, current_server
                downloads[current_server].downloaded = 0  # Reset progress
                server_history.append(current_server + 1)  # Record server switch
                start_time = time.time() # Reset start time after switch
                already_switched = True  # Mark that they've switched once
            else:
                print("\n\033[91mYou have already switched once and unfortunately cannot switch back. Continuing with the current server...\033[0m")


    end_time = time.time()
    total_time = end_time - overall_start_time
    # --- ECC Challenge ---
    challenge_data = ecc_challenge()
   
    print(challenge_data)
    
    print("\n\033[93mAnalyze the challenge data to recover the flag!\033[0m")
    print("\n\033[93mDecrypted Cipher Text2 : This is another important encrypted message.\033[0m")
    print("\033[92mHint: Using the decrypted second message, we can now decrypt the first message, which contains the secret flag.\033[0m")
    print("\n\033[92mYou might try writing a simple Python script that:")
    print("          1) Converts the hex-encoded ciphertexts into bytes.")
    print("          2) XORs the known-plaintext bytes with the second ciphertext (the known-plaintext one).")
    print("          3) Uses the result of that XOR to decrypt the first ciphertext and recover the hidden flag.")


    # --- Data Output ---
    data = {
        "condition": "1" if is_treatment else "0",
        "server_history": server_history,
        "download_completed": download_completed,
        "total_time": round(total_time, 2),
        "server1_time": round(server_times[0], 2),  # Time spent in Server 1
        "server2_time": round(server_times[1], 2),  # Time spent in Server 2
        "server1_progress": server_progress[0],  # Final progress in Server 1 (percentage)
        "server2_progress": server_progress[1],  # Final progress in Server 2 (percentage)
    }

    if switch_count > 0:
        data["switch_percentage"] = switch_percentage  # Percentage at which they switched

    if is_treatment:
        # Track throttle information for whichever server was initially selected
        throttled_server = initial_server_choice - 1
        # throttle_point PRINT
        data["tp"] = downloads[throttled_server].throttle_point * 100 if downloads[throttled_server].throttle_point else None
        # data["is_throttled"] = downloads[throttled_server].is_throttled
        if throttle_percentage is not None:
            data["throttle_percentage"] = throttle_percentage  # Actual percentage when throttling began

    print("\033[91mCopy the text below to Qualtrics to get compensation for this challenge.\033[0m")
    print("\n--- Study Data ---")
    for key, value in data.items():
        print(f"{key}: {value}")

    print("\033[91mCopy the text above to Qualtrics to get compensation for this challenge.\033[0m")



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="File Download Simulation")
    group = parser.add_mutually_exclusive_group()  # No longer required
    group.add_argument("--control", action="store_true", help="Run in control condition (no throttling)")
    group.add_argument("--treatment", action="store_true", help="Run in treatment condition (with throttling)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Command line args override global defaults
    if args.treatment:
        treatment_mode = True
    elif args.control:
        treatment_mode = False
    if args.debug:
        debug_mode = True

    main(treatment_mode, debug_mode)
