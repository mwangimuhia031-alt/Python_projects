# Caesar Cipher

A simple Python implementation of the Caesar cipher for encrypting and decrypting text using a shift value between 1 and 25.

## Overview

This program shifts each alphabetic character in a message by a fixed number of positions. It preserves the original case of letters and leaves non-letter characters unchanged.

## Features

- Encrypts plain text using a Caesar shift
- Decrypts encrypted text by reversing the shift
- Validates the shift value
- Supports uppercase and lowercase letters
- Ignores non-letter characters

## Functions

### `caesar(text, shift, encrypt=True)`

Applies the Caesar cipher transformation to the provided text.

- `text`: the message to encrypt or decrypt
- `shift`: the number of positions to shift
- `encrypt`: set to `True` for encryption and `False` for decryption

### `encrypt(text, shift)`

Convenience function to encrypt a message.

### `decrypt(text, shift)`

Convenience function to decrypt a message.

## Example

```python
from main import encrypt, decrypt

message = "Hello, World!"
encoded = encrypt(message, 3)
print(encoded)  # Khoor, Zruog!

decoded = decrypt(encoded, 3)
print(decoded)  # Hello, World!
```

## Example Output

```python
Pbhentr vf sbhaq va hayvxryl cynprf.
```

The script includes a sample encrypted string and decrypts it with a shift of 13, producing:

```python
"The secret is hidden in plain sight."
```

## Requirements

- Python 3.x

## Run the Script

```bash
python main.py
```

This will decrypt the sample encrypted text and print the result to the console.
