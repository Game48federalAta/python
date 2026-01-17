import string


iyelik_ekleri = [
    "ım",
    "im",
    "um",
    "üm",
    "ın",
    "in",
    "un",
    "ün",
    "ı",
    "i",
    "u",
    "ü",
    "ımız",
    "imiz",
    "umuz",
    "ümüz",
    "ınız",
    "iniz",
    "unuz",
    "ünüz",
    "ları",
    "leri",
]

hal_ekleri = [
    "ı",
    "i",
    "u",
    "ü",
    "a",
    "e",
    "da",
    "de",
    "tan",
    "ten",
    "dan",
    "den",
    "ın",
    "in",
    "un",
    "ün",
    "la",
    "le",
    "ca",
    "ce",
]
yapim_ekleri = [
    "ci",
    "cı",
    "cu",
    "cü",  # Meslek ve kişi bildiren ekler (öğrenci, işçi, çocuğu)
    "li",
    "lı",
    "lü",
    "lü",  # Bir yerin ya da şeyin niteliğini bildiren ekler (güzel, yeşil)
    "sal",
    "sel",  # Durum, özellik bildiren ekler (doğal, kültürel)
    "sız",
    "siz",  # Olumsuzluk, yokluk bildiren ekler (sussuz, şekersiz)
    "laş",
    "leş",  # Değişim ya da gelişim bildiren ekler (gelişmek, küçülmek)
    "ca",
    "ce",  # Yer belirten ekler (Türkçe, köylüce)
    "cı",
    "cık",
    "cik",  # Sıklık ya da yapma anlamı bildiren ekler (çalışkan, fakirlik)
    "cıklık",  # İyelik ve durum bildiren (yemekçilik, sanatçılık)
    "can",  # Durum ya da özne belirtir (acılı, korkunç)
    "lar",
    "ler",  # Çoğul ekleri
    "ık",
    "ik",
    "acak",
    "ecek",  # Gelecek zaman ve eylem bildiren ekler
    "dik",
    "tik",
    "dir",  # Koşul, olasılık ekleri
    "ık",
    "ik",
    "an",  # Süreç ya da hal ekleri (çalışan, okuyan)
    "ecek",
    "acak",  # Gelecek zaman eki
    "mak",
    "mek",  # Fiil yapım ekleri (yapmak, gitmek)
    "leşmek",
    "leşme",  # Değişim bildirir (büyümek, küçülmek)
    "abilmek",
    "ebilmek",  # Yeteneği gösteren ekler
    "tık",
    "tik",  # Durum belirtme (yavaşlatmak, yıkmak)
    "tik",
    "lik",  # Durum ya da şekil bildirir (güzelcilik, arkadaşlık)
    "cık",
    "cik",  # Durum ya da işlev bildirir (büyüklük, küçüklük)
    "lilemek",
    "lik",  # Durum ve özellik (sağlıklı, neşeli)
]

cogul_ekleri = ["lar", "ler"]
sesli_harfler=["a","e","i","ı","o","ö","u","ü"]
def get_seperate_words(text):
    text = text.translate(str.maketrans("", "", string.punctuation))  # Noktalama işaretlerini temizle
    text_ = text.split()  # Kelimeleri ayır
    return text_


def get_root(text):
    for ek in iyelik_ekleri:
        if  ek in text:
            text = text.replace(ek, "")
            break
    for ek in cogul_ekleri:
        if ek in text:
            text = text.replace(ek, "")
            break
    for ek in hal_ekleri:
        if ek in text:
            text = text.replace(ek, "")
            break
    

    return text

print(get_root("kitaplık"))
