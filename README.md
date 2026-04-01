# Type-D Message Authentication and Encryption (Myszkowski Cipher)

This repository contains a Python implementation of the **Type-D Authenticated Encryption** model. This architecture provides both **Confidentiality** (via encryption) and **Integrity/Authenticity** (via a keyed hash).

## 🛡️ The Security Model

The system follows the **Type-D** logic, which is mathematically represented as:

$$E_{K2} [M \ || \ H(M \ || \ S)]$$

Where:
* **M**: The original Plaintext Message.
* **S**: A Shared Secret (Salt) used for hashing.
* **H**: A Cryptographic Hash function (SHA-256).
* **K2**: The Encryption Key (Keyword) for the transposition cipher.
* **E**: The **Myszkowski Cipher** encryption algorithm.

## 🚀 The Algorithm

The process is broken down into 10 distinct steps:

### Phase 1: The Source (Sender)
1.  **Initialize $M$ and $S$**: Define the plaintext message and the shared secret.
2.  **Concatenate $M$ and $S$**: Combine them into a single string: $M \ || \ S$.
3.  **Generate the Hash ($H$)**: Hash the concatenated string to create the "Digital Seal."
4.  **Create Payload**: Attach the hash to the message: $[M \ || \ H(M \ || \ S)]$.
5.  **Prepare Myszkowski Key ($K_2$)**: Rank the keyword letters alphabetically. Repeating letters receive identical ranks.
6.  **Perform Encryption ($E$)**: Arrange the payload in a grid and transpose letters based on $K_2$ ranks (reading repeated column ranks row-by-row).

### Phase 2: The Destination (Receiver)
7.  **Receive and Decrypt ($D$)**: Use $K_2$ to reverse the transposition and recover the payload.
8.  **Split the Payload**: Extract the message ($M$) and the received hash. Padding characters ('X') are stripped before slicing.
9.  **Recalculate Hash**: The receiver generates a local hash using the extracted $M$ and their copy of $S$.
10. **Comparison**: Compare the *local hash* with the *received hash*. If they match, the message is verified.

## 💻 Implementation Details

### The Myszkowski Cipher
Unlike standard Columnar Transposition, the Myszkowski cipher handles keyword duplicates uniquely:
* **Unique Ranks**: The entire column is read top-to-bottom.
* **Repeated Ranks**: The columns are read together, row-by-row.

### Prerequisites
* Python 3.x
* `hashlib` (Standard Library)

## 🛠️ Usage

```python
# Define your parameters
msg = "CRYPTOGRAPHY"
secret = "MY_SECRET_SALT"
key = "TOMATO"

# Run the Type-D Workflow
run_type_d(msg, secret, key)
```

## 📝 Example Output

```text
--- SENDER SIDE ---
1. Generated Hash H(M||S): a48630e7
2. Payload to Encrypt: CRYPTOGRAPHYa48630e7
3. Final Ciphertext: PP6XYA8XRORY407XCTGHa3eX

--- RECEIVER SIDE ---
4. Decrypted Payload: CRYPTOGRAPHYa48630e7XXXX
5. Extracted Message: CRYPTOGRAPHY
   Extracted Hash: a48630e7

--- FINAL COMPARISON ---
SUCCESS: Hashes match. Message is authentic and confidential.
```

## ⚖️ License
This project is for educational purposes under the MIT License.
