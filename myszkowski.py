import hashlib
import math

def get_keyword_ranks(keyword):
    """Assigns ranks to the keyword. Duplicate letters get the same rank."""
    sorted_chars = sorted(list(set(keyword)))
    ranks = [sorted_chars.index(char) + 1 for char in keyword]
    return ranks

def myszkowski_encrypt(plaintext, keyword):
    ranks = get_keyword_ranks(keyword)
    num_cols = len(keyword)
    num_rows = math.ceil(len(plaintext) / num_cols)
    
    # Pad plaintext to fill the grid
    plaintext = plaintext.ljust(num_rows * num_cols, 'X')
    
    # Create the grid
    grid = [plaintext[i:i + num_cols] for i in range(0, len(plaintext), num_cols)]
    
    ciphertext = ""
    # Process ranks in numerical order
    unique_ranks = sorted(list(set(ranks)))
    
    for r in unique_ranks:
        # Find all columns with this rank
        col_indices = [i for i, val in enumerate(ranks) if val == r]
        
        if len(col_indices) == 1:
            # Standard Columnar: Read the single column top-to-bottom
            idx = col_indices[0]
            for row in range(num_rows):
                ciphertext += grid[row][idx]
        else:
            # Myszkowski Rule: Read multiple columns row-by-row
            for row in range(num_rows):
                for idx in col_indices:
                    ciphertext += grid[row][idx]
                    
    return ciphertext

def myszkowski_decrypt(ciphertext, keyword):
    ranks = get_keyword_ranks(keyword)
    num_cols = len(keyword)
    num_rows = len(ciphertext) // num_cols
    
    # Initialize empty grid
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    current_pos = 0
    unique_ranks = sorted(list(set(ranks)))
    
    for r in unique_ranks:
        col_indices = [i for i, val in enumerate(ranks) if val == r]
        
        if len(col_indices) == 1:
            idx = col_indices[0]
            for row in range(num_rows):
                grid[row][idx] = ciphertext[current_pos]
                current_pos += 1
        else:
            for row in range(num_rows):
                for idx in col_indices:
                    grid[row][idx] = ciphertext[current_pos]
                    current_pos += 1
                    
    # Read row-by-row to get payload
    return "".join("".join(row) for row in grid)

# --- TYPE D WORKFLOW ---

def run_type_d(message, secret, keyword):
    print(f"--- SENDER SIDE ---")
    # 1. Hashing: H(M || S)
    # Using first 8 chars of SHA-256 for a manageable ciphertext length
    hash_input = message + secret
    msg_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    print(f"1. Generated Hash H(M||S): {msg_hash}")

    # 2. Payload: M || Hash
    payload = message + msg_hash
    print(f"2. Payload to Encrypt: {payload}")

    # 3. Encryption: E(K, Payload)
    ciphertext = myszkowski_encrypt(payload, keyword)
    print(f"3. Final Ciphertext: {ciphertext}\n")

    print(f"--- RECEIVER SIDE ---")
    # --- RECEIVER SIDE ---
    # 4. Decryption: D(K, Ciphertext)
    decrypted_payload = myszkowski_decrypt(ciphertext, keyword)
    
    # STEP 1: Remove the 'X' padding FIRST
    clean_payload = decrypted_payload.rstrip('X') 
    
    # 5. Extraction
    received_msg = clean_payload[:-8]
    received_hash = clean_payload[-8:]
    
    print(f"5. Extracted Message: {received_msg}")
    print(f"   Extracted Hash: {received_hash}")

    # 6. Verification: Recalculate Hash
    check_hash = hashlib.sha256((received_msg + secret).encode()).hexdigest()[:8]
    
    print(f"\n--- FINAL COMPARISON ---")
    if check_hash == received_hash:
        print("SUCCESS: Hashes match. Message is authentic and confidential.")
    else:
        print("FAILURE: Hash mismatch! The message has been tampered with.")

# Example execution
msg = "CRYPTOGRAPHY"
sec = "SECRET123"
key = "TOMATO"

run_type_d(msg, sec, key)