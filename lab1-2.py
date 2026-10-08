ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
N = len(ALPHABET)


def get_permutation(kw):
    # remove char duplicates
    unique_chars = ""
    for char in kw:
        if char not in unique_chars:
            unique_chars += char

    # add the remaining letters
    for char in ALPHABET:
        if char not in unique_chars:
            unique_chars += char

    return unique_chars


def get_keyword():
    while True:
        kw = input("Choose a keyword: ")

        if len(set(kw)) < 7:
            print("Keyword cannot be less than 7 characters.")
            continue

        for char in kw:
            if char not in ALPHABET:
                print("Keyword must include only letters of the Romanian alphabet")

        return kw.upper()


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


def caesar_cipher(text, key, permutation, operation):
    result = ""

    for char in text:
        index = permutation.index(char)

        if operation == "E":
            new_index = (index + key) % N
        else:
            new_index = (index - key) % N

        result += permutation[new_index]

    return result


operation = get_operation()
key = get_key()
keyword = get_keyword()
text = get_text()
permutation = get_permutation(keyword)

result = caesar_cipher(text, key, permutation, operation)
print("Result:", result)
