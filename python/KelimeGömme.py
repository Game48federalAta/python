from transformers import pipeline

# Özetleme pipeline'ını oluştur
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Özetlenecek metin
text = """
Yapay zeka, insan zekasını taklit eden makinelerin ve bilgisayar sistemlerinin geliştirilmesiyle ilgilenen bir bilim dalıdır.
Yapay zeka uygulamaları, dil işleme, görüntü tanıma, robotik, ve daha birçok alanda kullanılmaktadır. 
Bu teknoloji, makinelerin öğrenme, anlama, ve karar verme yeteneklerini geliştirmeyi amaçlar.
"""

# Metni özetle
summary = summarizer(text)
print("Modelin Tahmini : ",format(summary[0]["summary_text"]))
