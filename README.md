# 🛡️ MakingRansomware (Educational Python Project)

This repository demonstrates **how ransomware works internally** using Python.  
It includes file encryption/decryption, RSA key generation, and a simulated ransomware flow.

> ⚠️ **Disclaimer:**  
> This project is strictly for educational purposes.  
> Do **not** use this code on systems you do not own. Unauthorized use is illegal.

---

[![Making Ransomware Demo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://wwwyoutube.com/watch?v=lYW5gbkp4VA)

## 📋 Project Structure

All files are in the same folder:
PubKeyCreate.py # Generate RSA keys
Ransomware.py # Encrypt files
Receiver.py # Simulate attacker receiving key
DecryptRSA.py # Decrypt symmetric key
Decrypt..py # Decrypt files


---

## 🛠️ Requirements

- Python 3.x
- Install required library:

```bash
pip install cryptography
```
🚀 Step-by-Step Tutorial & Execution Flow
⚠️ Important Warning (Read Before Running):
Always create a separate test folder (e.g., test_folder/) and place only dummy files inside it for experimentation. DO NOT run this script in important directories such as Desktop, Documents, or Downloads.

1️⃣ Generate RSA Keys
First, you need to generate the attacker's asymmetric key pair.
```bash
python PubKeyCreate.py
```
Output: public.pem and private.pem will be generated.

2️⃣ Setup the Target Folder (Victim's Machine)
Prepare the directory you want to simulate an attack on.

Move public.pem into your target test folder.

Move Ransomware.py into the same target test folder.

3️⃣ Start the Attacker's Server
Before running the ransomware, the attacker's receiving server needs to be online. Open a new terminal and run:

```bash
python Receiver.py
```
(The server is now listening for incoming connections...)

4️⃣ Execute the Ransomware (Simulate Attack)
Go to the terminal pointing to your target test folder and execute the ransomware:

```bash
python Ransomware.py
```
What happens here:

The script steals (exfiltrates) the original files and sends them to the Receiver.

It generates a symmetric master key and encrypts all files in the folder.

It encrypts the symmetric master key using public.pem and sends it to the Receiver.

On the attacker's side (Receiver terminal), you will see a new folder named ReceivedFiles containing the stolen files and master.key.enc.

5️⃣ Decrypt the Master Key (Attacker's Side)
To decrypt the victim's files, you first need to decrypt the symmetric key.

Move your private.pem and DecryptRSA.py into the newly created ReceivedFiles directory.

Run the RSA decryption script inside that folder:

```bash
python DecryptRSA.py
```
Output: This will decrypt master.key.enc and yield the usable symmetric key (e.g., master.key).

6️⃣ Decrypt the Victim's Files
Finally, simulate the victim receiving the decryption key to restore their files.

Move the decrypted master key and Decrypt.py into the original encrypted target folder.

Run the decryption script:

```bash
python Decrypt.py
```
Result: All encrypted files in the folder will be restored to their original state! 🎉
