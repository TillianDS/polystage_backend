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

# Example usage
print(generate_password())
