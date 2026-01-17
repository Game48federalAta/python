from collections import Counter
import re


def find_keys_by_value(my_dict, target_value):
    keys = [key for key, value in my_dict.items() if value == target_value]
    return keys


def bow(text):
    # Küçük harflere dönüştür ve özel karakterleri temizle
    text = text.lower()
    words = re.findall(r"\b\w+\b", text)

    # Kelimelerin frekansını hesapla
    word_count = Counter(words)

    try:
        return find_keys_by_value(word_count,max(word_count.values()))
    except IndexError:
        return text

# Örnek kullanım
#sample_text = "Fatih Sultan Mehmed, 3 Mayıs 1481'de Gebze'de vefat etti. Ölümü, Osmanlı İmparatorluğu için büyük bir kayıp olarak değerlendirildi. Ancak, onun mirası, imparatorluğun genişlemesi ve dönüşümündeki katkılarıyla tarihte önemli bir yer edinmiştir. İstanbul’daki izleri, onun etkisinin günümüze kadar sürdüğünü gösterir."


#bow_result = bow(sample_text)
#print(bow_result)
