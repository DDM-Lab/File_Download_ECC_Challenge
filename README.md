# sunk-cost

  

# ECC Crypto Challenge

  

This project simulates a secure file download which includes an Elliptic Curve Cryptography (ECC) challenge. It demonstrates variable download rates, user interaction, and a cryptographic vulnerability using ECC with reused nonces.

  
 

## Requirements

  

- Python 3.6 or above

- cryptography library

  

## Installation

  

1. Clone this repository or download the script.

```

git clone https://github.com/saketh7502/Sunk_Cost_DDMLab.git

```

  

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

  

**Carolina**: The participants will not see this, correct? Additionally, diference between the servers depends on if the particpant was assigned to the control or treatment groups.

  

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


  
  

## Control and treatment conditions:

  

Control Condition: Participants experience uninterrupted file downloads without throttling or delays.

Treatment Conditions: Participants encounter file download throttling at varying stages:

Throttle at 50%, 60%, 70%, 80%, 90%

  
  




## Carolina's Feedback


- Provide a better explanation of what the user is downloading and why. - The text "--- Welcome to the ECC Crypto Challenge! ---" should appear in the beginning before the download starts. And more context should be given. For example:

> "Download the encrypted files from the server of your choice to begin the challenge."

- And if we want to keep the storytelling data, we should incorporate that from the beginning instead of just showing it at the end:

> "Analyze the challenge data to recover the flag!
>Robin Hood, in his clever quest to outsmart the Sheriff of Nottingham, has provided us with the decrypted second message: 'This is another encrypted message.'/n Using this information, we can now decrypt the first message, which contains the secret flag.
>Hint: Repetition is the enemy of security."

- At the beginning, inform users that they can switch servers at any time but warn them about the potential consequences :

> Message: "You can switch servers at any point during the download, but doing so will reset your progress. Choose wisely!"

- They should always know they can switch. The option to switch shouldn't appear only after the throttling has begun.

- Right now, the control and treatment are not implemented(?)

- Right now, when I switched, the download restarted in the new server, but I didn't lose progress by switching (I didn't start at zero after switching)

- I would remove the option for the participant not to see the challenge data. They should always get to see it, and should say "no".

- Right now, If I say I don't want to switch I can no longer decided to switch, but I should be able to switch 


- Before switching, ask for confirmation (suggestion):

> Message: "Switching servers will reset your download progress. Are you sure you want to switch? (yes/no)."

- At the end, we should have the time they took when the throttling began and if they switched:

### Example output:

```Download Analysis:

- Total Download Time: 45 seconds

- Number of Server Switches: 0

- Throttling began at: 80%```