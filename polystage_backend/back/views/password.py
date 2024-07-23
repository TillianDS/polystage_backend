import random
import string

special_characters = r"[()[\]{}|\\`~!@#$%^&*_\-+=;:\"',<>./?]"

def generate_password(length=9):
    if length < 7:
        raise ValueError("Password length must be at least 7 characters")

    # Characters to choose from
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits

    # Ensure the password has at least one of each required character type
    password = [
        random.choice(special_characters),
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits)
    ]

    # Fill the rest of the password length with random choices from all allowed characters
    all_characters = uppercase_letters + lowercase_letters + digits
    password += random.choices(all_characters, k=length - 4)

    # Shuffle the resulting list to ensure randomness
    random.shuffle(password)

    # Convert list to string and return
    return ''.join(password)

def verify_passsword (self, password1, password2, request) :
        
        password_length = 7

        if password1 != password2:
            return {"error": "Les mots de passe ne correspondent pas"}
        if len(password1) < password_length:
            return {"error": f"Le mot de passe doit contenir au moins {password_length} caractères"}
        if not any(char.islower() for char in password1):
            return {"error": "Le mot de passe doit contenir au moins une lettre minuscule"}
        if not any(char.isupper() for char in password1):
            return {"error": "Le mot de passe doit contenir au moins une lettre majuscule"}
        if not any(char in special_characters for char in password1):
            return {"error": "Le mot de passe doit contenir au moins un caractère spécial"}
        
        return True