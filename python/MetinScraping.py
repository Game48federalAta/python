from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from datasets import load_dataset

# Model ve tokenizer'ı yükle
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# IMDb veri setini yükle ve ilk 1000 örneği al
dataset = load_dataset("imdb")
small_dataset = {
    "train": dataset["train"]
    .shuffle(seed=42)
    .select([i for i in list(range(1000))]),  # 1000 eğitim örneği
    "test": dataset["test"]
    .shuffle(seed=42)
    .select([i for i in list(range(500))]),  # 500 test örneği
}

# Eğitim argümanları
training_args = TrainingArguments(
    output_dir="./results",  # Çıktı dizini
    num_train_epochs=1,  # Eğitim döngüleri
    per_device_train_batch_size=16,  # Batch boyutu
    per_device_eval_batch_size=64,  # Değerlendirme batch boyutu
    warmup_steps=500,  # Warmup adımları
    weight_decay=0.01,  # Ağırlık azalması
    logging_dir="./logs",  # Log dizini
)

# Trainer'ı oluştur
trainer = Trainer(
    model=model,  # Eğitilecek model
    args=training_args,  # Eğitim argümanları
    train_dataset=small_dataset["train"],  # Eğitim verisi
    eval_dataset=small_dataset["test"],  # Değerlendirme verisi
)

# Modeli eğit
trainer.train()

# Modelin değerlendirilmesi
trainer.evaluate()

# Modeli kaydet
model.save_pretrained("./my_model")
tokenizer.save_pretrained("./my_model")
