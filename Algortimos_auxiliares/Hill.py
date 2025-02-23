import time
from math import gcd

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_inverse(matrix, modulus):
    a, b = matrix[0]
    c, d = matrix[1]
    det = (a * d - b * c) % modulus
    det_inv = mod_inverse(det, modulus)
    if det_inv is None:
        return None
    inv_matrix = [
        [d * det_inv % modulus, (-b) * det_inv % modulus],
        [(-c) * det_inv % modulus, a * det_inv % modulus]
    ]
    return inv_matrix

def decrypt(ciphertext, inv_key):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        pair = ciphertext[i:i+2]
        if len(pair) < 2:
            pair += 'x'
        nums = [ord(char) - ord('a') for char in pair]
        dec_nums = [
            (inv_key[0][0] * nums[0] + inv_key[0][1] * nums[1]) % 26,
            (inv_key[1][0] * nums[0] + inv_key[1][1] * nums[1]) % 26
        ]
        plaintext += "".join(chr(n + ord('a')) for n in dec_nums)
    return plaintext

expected_frequencies = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57,
    'f': 1.02, 'g': 1.30, 'h': 1.28, 'i': 6.18, 'j': 0.40,
    'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05, 'o': 10.73,
    'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34,
    'u': 4.63, 'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01, 'z': 0.47
}

def chi_squared_stat(text):
    text = text.lower()
    n = len(text)
    chi2 = 0
    for letter, freq in expected_frequencies.items():
        observed = text.count(letter)
        expected = n * (freq / 100)
        if expected > 0:
            chi2 += (observed - expected) ** 2 / expected
    return chi2

ciphertext = input("Insira o texto cifrado: ")

start_time = time.time()
attempts = 0

best_score = float('inf')
best_key = None
best_plaintext = None

for a in range(26):
    for b in range(26):
        for c in range(26):
            for d in range(26):
                det = (a * d - b * c) % 26

                if gcd(det, 26) != 1:
                    continue
                key = [[a, b], [c, d]]
                inv_key = matrix_inverse(key, 26)
                if inv_key is None:
                    continue
                decrypted = decrypt(ciphertext, inv_key)
                score = chi_squared_stat(decrypted)
                attempts += 1

                if attempts % 10000 == 0:
                    elapsed = time.time() - start_time
                    print(f"Chaves testadas: {attempts} - Tempo decorrido: {elapsed:.2f} s - Melhor chi² até agora: {best_score:.2f}")

                if score < best_score:
                    best_score = score
                    best_key = key
                    best_plaintext = decrypted

print("\nResultado final:")
print("Melhor chave encontrada:", best_key)
print("Chi-quadrado:", best_score)
print("Mensagem decifrada:", best_plaintext)

