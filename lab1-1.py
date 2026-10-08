ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
N = len(ALPHABET)


def get_operation():
    while True:
        operation = input("Choose E (encrypt) or D (decrypt): ").upper()

        if operation in ("E", "D"):
            return operation

        print("Invalid operation. Enter E or D.")


def get_key():
    while True:
        try:
            key = int(input("Enter a key (1-30): "))

            if 1 <= key <= 30:
                return key

            print("Invalid key. Allowed range: 1 to 30.")

        except ValueError:
            print("Invalid key. Enter an integer from 1 to 30.")


def get_text():
    while True:
        text = input("Enter your message: ").upper()
        text = text.replace(" ", "")

        invalid = None

        for char in text:
            if char not in ALPHABET:
                invalid = char
                break

        if invalid is not None:
            print(f"Invalid character: '{invalid}'.")
            print("Only Romanian letters A-Z, Ă, Â, Î, Ș, Ț and spaces are allowed.")
        elif not text:
            print("The message cannot be empty.")
        else:
            return text


def caesar_cipher(text, key, operation):
    result = ""

    for char in text:
        index = ALPHABET.index(char)

        if operation == "E":
            new_index = (index + key) % N
        else:
            new_index = (index - key) % N

        result += ALPHABET[new_index]

    return result


operation = get_operation()
key = get_key()
text = get_text()

result = caesar_cipher(text, key, operation)

print("Result:", result)
