import cipher
import csv
import string
import numpy as np
from random import choice


def rand_string(size=6, chars=string.ascii_lowercase):
    output = []
    for i in range(size):
        output.append(choice(chars))
        while output[i] == '.' and output[i - 1] == '.':  # no two dots in a row
            output[i] = choice(chars)

    while output[size - 1] == '.':
        output[size - 1] = choice(chars)
    return ''.join(output)


cipher_prompts = np.array(["i like pizza", "you are a great person", "zebra", "yatch", "they watch tv with a dog while reading"])

for prompt in cipher_prompts:
    for i in range(100):  # amount of ciphers to generate
        key = rand_string()
        encrypted = cipher.encrypt(prompt, key)
        decrypted = cipher.decrypt(encrypted, key)

        with open('cipher_data.csv', 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([decrypted, encrypted, key])
