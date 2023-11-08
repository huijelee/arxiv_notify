from cryptography.fernet import Fernet

# Generate a key and instantiate a Fernet instance
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the key to a file
with open('data/filekey.key', 'wb') as filekey:
   filekey.write(key)

# Given a dictionary of your credentials
email = input('your email: ')
password = input('your password: ')
credentials = {
    "email": email,
    "password": password
}

# Convert the credentials dictionary to a JSON string
import json
credentials_str = json.dumps(credentials).encode('utf-8')

# Encrypt the credentials string
encrypted_account = cipher_suite.encrypt(credentials_str)

# Write the encrypted credentials to a file
with open('data/encrypted_account', 'wb') as encrypted_file:
    encrypted_file.write(encrypted_account)

print("Credentials have been encrypted and saved.")

