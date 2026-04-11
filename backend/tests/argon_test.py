from argon2 import PasswordHasher
ph = PasswordHasher()

print(ph.hash("12334"))