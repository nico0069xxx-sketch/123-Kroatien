#!/usr/bin/env python3
"""
Secret Key Generator
Generiert einen sicheren SECRET_KEY für Django

Verwendung:
    python generate_secret_key.py
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generiert einen sicheren SECRET_KEY"""
    
    # Zeichen für den Key
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Sicheren Key generieren
    secret_key = ''.join(secrets.choice(chars) for _ in range(length))
    
    return secret_key

if __name__ == '__main__':
    key = generate_secret_key()
    print("\n" + "="*60)
    print("NEUER SECRET_KEY GENERIERT:")
    print("="*60)
    print(f"\n{key}\n")
    print("="*60)
    print("\nFügen Sie diesen Key in Ihre .env Datei ein:")
    print(f"SECRET_KEY={key}")
    print("="*60 + "\n")
