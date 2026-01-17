import yt_dlp


def download_youtube_video(url):
    # İndirme seçeneklerini ayarlama
    ydl_opts = {
        "format": "bestaudio/best",  # En iyi ses kalitesini seç
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Ses dosyasını MP3'e dönüştür
                "preferredcodec": "mp3",  # MP3 formatı
                "preferredquality": "192",  # Ses kalitesi
            }
        ],
    }

    # yt-dlp ile indirme işlemi
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


"""import os
import tkinter as tk
from tkinter import Listbox

# Müziklerin olduğu klasör
music_folder = "./"

# Pencere oluştur
root = tk.Tk()
root.title("Müzik Listesi")
root.geometry("300x400")

# Listbox oluştur
music_listbox = Listbox(root, width=50, height=20)
music_listbox.pack(padx=10, pady=10)

# Klasördeki müzikleri listele
if os.path.exists(music_folder):
    for file in os.listdir(music_folder):
        if file.endswith(".mp3") or file.endswith(
            ".wav"
        ):  # Sadece müzik dosyalarını al
            music_listbox.insert(tk.END, file)

root.mainloop()"""


"""if __name__ == "__main__":
    video_url = input("YouTube video URL'sini girin: ")
    download_youtube_video(video_url)"""
import requests


def download_thumbnail(video_url, save_path):
    # Video URL'sinden video ID'sini çıkart
    video_id = video_url.split("v=")[-1].split("&")[0]

    # Thumbnail URL'si
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    # Thumbnail'ı indir
    response = requests.get(thumbnail_url)

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Thumbnail başarıyla indirildi: {save_path}")
    else:
        print("Thumbnail indirilemedi.")


# Kullanım
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Örnek video URL'si
save_path = "thumbnail.jpg"  # Kaydedilecek dosya adı

download_thumbnail(video_url, save_path)
