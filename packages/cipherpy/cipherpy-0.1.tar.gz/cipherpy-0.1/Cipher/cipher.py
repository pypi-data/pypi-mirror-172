letters = "abcdefghijklmnopqrstuvwxyz"


# Shifts each letter in the text by the given amount
def cesear_shift(text, shift):
    output = ""
    text = text.lower()
    for letter in text:
        if letter in letters:
            output += letters[(letters.index(letter) + shift) % 26]
        else:
            output += letter
    return output


def cesear_shift_list(words, shift):
    output = []
    for word in words:
        if shift == "length":
            output.append(cesear_shift(word, len(word)))
        elif shift == "-length":
            output.append(cesear_shift(word, -len(word)))
        else:
            output.append((cesear_shift(word, shift)))
    return output


def cesear_shift_every_letter_by_key(text, key, operation):
    output = text.copy()
    for i in range(len(text)):  # for each word
        output[i] = list(text[i]) # convert to list so we can change each letter
        word = text[i]
        for j in range(len(word)):  # for each letter in the word
            letter_in_input = word[j]
            if letter_in_input not in letters:
                output[i][j] = letter_in_input
            elif operation == "encrypt":
                # Shifts the entire word based on each letter of key's position in the alphabet
                for letter_in_key in key:
                    output[i][j] = cesear_shift(letter_in_input, letters.index(letter_in_key) + 1)
            elif operation == "decrypt":
                # Shifts the entire word back based on each letter of the key's position in the alphabet
                for letter_in_key in key:
                    output[i][j] = cesear_shift(letter_in_input, -letters.index(letter_in_key) - 1)
        output[i] = "".join(output[i])  # convert back to string
    return output


def separate_words(text):
    output = []
    word = ""
    for letter in text:
        if letter == " ":
            output.append(word)
            word = ""
        else:
            word += letter
    output.append(word)
    return output


def join_words(words):
    output = ""
    for i in range(len(words)):
        word = words[i]
        if i == len(words) - 1:
            output += word
        else:
            output += word + " "
    return output


def lower_text_list(list):
    output = []
    for word in list:
        output.append(word.lower())
    return output


def move_half_to_end(text):
    output = ""
    first_half = ""
    for i in range(len(text)):
        if i < len(text) / 2:
            first_half += text[i]
        else:
            output += text[i]

    output += first_half
    return output


def move_half_to_start(text):
    output = ""
    second_half = ""

    for i in range(len(text)):
        if i > len(text) / 2:
            second_half += text[i]
        else:
            output += text[i]

    output = second_half + output
    return output


print(move_half_to_start("hello"))


def encrypt(text, key):
    cipher = separate_words(text)
    cipher = lower_text_list(cipher)
    for i in range(len(text)):
        cipher = cesear_shift_list(cipher, "length")
        cipher = cesear_shift_every_letter_by_key(cipher, key, "encrypt")

    cipher = join_words(cipher)
    # cipher = move_half_to_end(cipher)
    return cipher


def decrypt(text, key):
    cipher = separate_words(text)
    for i in range(len(text)):
        cipher = cesear_shift_every_letter_by_key(cipher, key, "decrypt")
        cipher = cesear_shift_list(cipher, "-length")

    cipher = join_words(cipher)
    return cipher
