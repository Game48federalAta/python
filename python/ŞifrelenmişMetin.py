import random
import string

# Türk alfabesi şifreleme haritası
custom_alphabet = {
    "a": "1",
    "b": "c",
    "c": "x",
    "ç":".",
    "d": "m",
    "e": "7",
    "f": "y",
    "g": "t",
    "ğ":",",
    "h": "2",
    "ı": "9",
    "i": "r",
    "j": "s",
    "k": "5",
    "l": "0",
    "m": "z",
    "n": "4",
    "o": "q",
    "ö": "3",
    "p": "8",
    "r": "6",
    "s": "v",
    "ş": "f",
    "t": "b",
    "u": "j",
    "ü": "w",
    "v": "d",
    "y": "_",
    "z": "[",
    " ": " ",
}

# Şifre çözme haritası (otomatik oluşturuluyor)
reverse_mapping = {v: k for k, v in custom_alphabet.items()}

# Global değişkenler
matched_letters = {}  # Doğru tahminler (şifreli -> açık metin)
wrong_guesses = {}  # Yanlış tahminler (şifreli harf -> yanlış karakterler)
alfb = {char: 0 for char in custom_alphabet.keys()}  # Alfabe durumu




def clean_text(text):
    """
    Verilen metindeki tüm noktalama işaretlerini kaldırır ve
    tüm büyük harfleri küçük harfe çevirir.

    Args:
        text (str): Düzenlenecek metin.

    Returns:
        str: Düzenlenmiş metin.
    """
    # Tüm noktalama işaretlerini kaldır
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Büyük harfleri küçük harfe çevir
    text = text.lower()

    return text


def encrypt(text):
    """Verilen metni custom_alphabet kullanarak şifreler."""
    return "".join(custom_alphabet.get(char, char) for char in text)


def decrypt(text):
    """Şifreli metni custom_alphabet'in ters haritası ile çözer."""
    return "".join(
        reverse_mapping.get(char, "?") for char in text
    )  # Bilinmeyen karakterler '?' olur.


def random_text(length):
    """Belirtilen uzunlukta rastgele harflerden oluşan bir metin oluşturur."""
    possible_chars = list(custom_alphabet.keys())
    return "".join(random.choice(possible_chars) for _ in range(length))


def get_matched_letters(encrypt_text, result_text):
    """Doğru ve yanlış tahmin edilen harfleri belirler."""
    original_text = decrypt(encrypt_text)
    for i, char in enumerate(result_text):
        if i < len(original_text) and char == original_text[i]:
            matched_letters[encrypt_text[i]] = original_text[i]
            alfb[char] = 2  # Doğru harf bulundu
        else:
            if encrypt_text[i] not in matched_letters:
                wrong_guesses.setdefault(encrypt_text[i], set()).add(char)
                alfb[char] = 1  # Yanlış harf işaretlendi


def all_letters_matched(encrypt_text):
    """Tüm şifreli harflerin doğru tahmin edilip edilmediğini kontrol eder."""
    return all(char in matched_letters for char in encrypt_text)


def get_next_guess():
    """Daha önce yanlış denenmemiş harfi seçer."""
    possible_chars = [c for c in custom_alphabet.keys() if alfb[c] == 0]
    return (
        possible_chars[0]
        if possible_chars
        else random.choice(list(custom_alphabet.keys()))
    )


def main(encrypt_text):
    """Şifreyi çözme süreci."""
    original_text = decrypt(encrypt_text)
    result_text = random_text(len(encrypt_text))
    attempt = 0

    while not all_letters_matched(encrypt_text):
        attempt += 1
        get_matched_letters(encrypt_text, result_text)

        unknown_indices = [
            i
            for i, char in enumerate(result_text)
            if encrypt_text[i] not in matched_letters
        ]

        if len(unknown_indices) == 1:
            # Sadece 1 bilinmeyen kaldıysa, sırayla dene
            last_index = unknown_indices[0]
            last_char = encrypt_text[last_index]
            result_text = (
                result_text[:last_index]
                + get_next_guess()
                + result_text[last_index + 1 :]
            )
        else:
            # Normal tahmin süreci
            result_text = "".join(
                matched_letters.get(
                    char,
                    random.choice(
                        [
                            c
                            for c in custom_alphabet.keys()
                            if c not in wrong_guesses.get(char, set())
                        ]
                    ),
                )
                for char in encrypt_text
            )

        # Tek bir print içinde tüm bilgileri göster
        print(
            f"[{attempt}] Şifreli: {encrypt_text} ->Çözülen: {result_text} |Gerçek: {original_text}"
        )

    print(f"\n✅ Şifre başarıyla çözüldü! {attempt} denemede bulundu.")


# Test metni
code = clean_text("")
encrypted_code = encrypt(code)
print(f"🛑 Şifreli Metin: {encrypted_code}")  # Şifreli metni göster
main(encrypted_code)
