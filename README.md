# File Download Simulation and ECC Crypto Challenge

This Python script simulates a file download process across two servers, incorporating a treatment/control condition. Additionally, it features an Elliptic Curve Cryptography (ECC) challenge that highlights the vulnerability of reusing nonces in encryption.

## Overview

The script is designed for two primary purposes:

1.  **Simulate File Downloads:** Users can choose to download a file from one of two servers. In the "treatment" condition, Server 1 experiences progressive throttling. The script tracks server switches, download times, and other relevant metrics for analysis.

2.  **ECC Crypto Challenge:** Presents a cryptographic challenge that demonstrates the security implications of reusing nonces in ECC encryption. The challenge provides encrypted messages and public keys, tasking the user with recovering the original message.

## Features

*   **Server Switching:** Users can switch between servers during the download process by pressing `CTRL+C`.
*   **Progress Bar:** Provides a visual representation of the download progress.
*   **ECC Crypto Challenge:** Includes an interactive challenge to test understanding of cryptographic vulnerabilities.
*   **Data Collection:** Gathers data on download behavior, server switches, and completion times for analysis.

## Getting Started

### Prerequisites

*   Python 3.6+
*   Cryptography Library: `pip install cryptography`

### Running the Script

1.  **Clone the Repository:** (If applicable, if you have this code hosted on GitHub, for example)

    ```
    git clone https://github.com/saketh7502/File_Download_Challenge.git
    cd File_Download_Challenge
    ```

2.  **Run the script with the desired condition:**

    *   **Control Condition (no throttling):**

        ```
        python main.py --control
        ```

    *   **Treatment Condition (with throttling):**

        ```
        python main.py --treatment
        ```

    *   **Debug Mode (optional):** Adds additional print statements to help understand the logic

        ```
        python main.py --treatment --debug
        ```

        or

        ```
           python main.py --control --debug
        ```

### Interacting with the Script

*   The script will prompt you to choose a server (1 or 2).
*   The download progress will be displayed in the console.
*   You can switch servers at any time by pressing `CTRL+C`. Note that switching servers will reset your download progress.
*   After the download (successful or cancelled), the ECC Crypto Challenge will be presented.
*   Finally, the script will output collected data related to the download process.

## ECC Crypto Challenge Details

The ECC challenge involves two messages encrypted using the same nonce, which is a critical vulnerability.  Here's a breakdown:

1.  **Encryption Scheme:** The script uses Elliptic-Curve Diffie-Hellman (ECDH) for key exchange and AES-GCM for symmetric encryption.

2.  **Vulnerability:** Reusing the same nonce with the same key in AES-GCM allows an attacker to perform XOR operations on the ciphertexts to potentially recover the plaintext.

3.  **Challenge:** The script provides:

    *   The sender's public key.
    *   Nonce 1
    *   Ciphertext 1
    *   Nonce 2
    *   Ciphertext 2

    Your task is to analyze the provided data, exploit the nonce reuse vulnerability, and recover the original message contained within `ciphertext1`.

4.  **Hints:** Two Hints are Provided for the Challenge after the download and during the display of challenge data.

## Data Output

At the end of the script's execution, the following data is printed to the console:

*   `condition`: Whether the script was run in "Treatment" or "Control" mode.
*   `initial_server_choice`: The server initially selected by the user.
*   `server_switches`: The number of times the user switched servers.
*   `server_history`: A list showing the sequence of servers used.
*   `download_completed`: A boolean indicating whether the download completed successfully.
*   `total_time`: The total time taken for the download process.
*   `throttle_point`: (Only in treatment) The point at which throttling began on Server 1.
*   `is_throttled`: (Only in treatment) A boolean indicating if Server 1 experienced throttling.

This data is intended to be copied and pasted into a survey or data collection tool (e.g. Qualtrics) for further analysis.


