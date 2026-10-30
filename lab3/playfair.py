ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
FILLERS = "12345"
SIZE = 6
PAD = "X"
ALT_PAD = "Q"


def normalize(text):
    # cedilla variants are produced by some keyboards
    text = text.replace("ş", "ș").replace("Ş", "Ș").replace("ţ", "ț").replace("Ţ", "Ț")
    return text.upper().replace(" ", "")


def find_invalid(text, allowed):
    for char in text:
        if char not in allowed:
            return char
    return None


def get_operation():
    while True:
        operation = input("Choose E (encrypt) or D (decrypt): ").upper()

        if operation in ("E", "D"):
            return operation

        print("Invalid operation. Enter E or D.")


def get_key():
    while True:
        key = normalize(input("Enter the key (at least 7 letters): "))
        invalid = find_invalid(key, ALPHABET)

        if invalid is not None:
            print(f"Invalid character: '{invalid}'.")
            print("Only Romanian letters A-Z, a-z, Ă, Â, Î, Ș, Ț are allowed.")
        elif len(key) < 7:
            print("The key cannot be shorter than 7 letters.")
        else:
            return key


def get_text(operation):
    if operation == "E":
        prompt, allowed = "Enter the message: ", ALPHABET
        hint = "Only Romanian letters A-Z, a-z, Ă, Â, Î, Ș, Ț and spaces are allowed."
    else:
        prompt, allowed = "Enter the cryptogram: ", ALPHABET + FILLERS
        hint = "Only Romanian letters A-Z, a-z, Ă, Â, Î, Ș, Ț, digits 1-5 and spaces are allowed."

    while True:
        text = normalize(input(prompt))
        invalid = find_invalid(text, allowed)

        if invalid is not None:
            print(f"Invalid character: '{invalid}'.")
            print(hint)
        elif not text:
            print("The text cannot be empty.")
        elif operation == "D" and len(text) % 2 != 0:
            print("The cryptogram must have an even number of characters.")
        else:
            return text


def build_matrix(key):
    chars = ""
    for char in key + ALPHABET + FILLERS:
        if char not in chars:
            chars += char

    matrix = [chars[i:i + SIZE] for i in range(0, SIZE * SIZE, SIZE)]
    pos = {}
    for r, row in enumerate(matrix):
        for c, char in enumerate(row):
            pos[char] = (r, c)

    return matrix, pos


def pad_for(char):
    return ALT_PAD if char == PAD else PAD


def prepare(text):
    pairs = []
    i = 0

    while i < len(text):
        a = text[i]

        if i + 1 == len(text):
            pairs.append(a + pad_for(a))
            i += 1
        elif text[i + 1] == a:
            pairs.append(a + pad_for(a))
            i += 1
        else:
            pairs.append(a + text[i + 1])
            i += 2

    return pairs


def split_pairs(text):
    return [text[i:i + 2] for i in range(0, len(text), 2)]


def playfair(pairs, matrix, pos, step):
    result = ""

    for a, b in pairs:
        r1, c1 = pos[a]
        r2, c2 = pos[b]

        if r1 == r2:
            result += matrix[r1][(c1 + step) % SIZE] + matrix[r2][(c2 + step) % SIZE]
        elif c1 == c2:
            result += matrix[(r1 + step) % SIZE][c1] + matrix[(r2 + step) % SIZE][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]

    return result


operation = get_operation()
key = get_key()
text = get_text(operation)
matrix, pos = build_matrix(key)

print("\nMatrix:")
for row in matrix:
    print(" ".join(row))
print()

if operation == "E":
    pairs = prepare(text)
    print("Pairs: ", " ".join(pairs))
    print("Result:", playfair(pairs, matrix, pos, 1))
else:
    pairs = split_pairs(text)
    print("Pairs: ", " ".join(pairs))
    print("Result:", playfair(pairs, matrix, pos, -1))
