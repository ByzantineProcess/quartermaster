import random

phrases = [
    "Don't give up your hour now! You're so close to finishing!",
    "Keep hacking! Stick to your hour!",
    "Go on, keep coding! Ships go rusty after time...",
    "Don't get distracted, keep your hour going!"
]

def get_motivation():
    return random.choice(phrases)