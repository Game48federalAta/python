import tkinter as tk
from tkinter import Scrollbar, Canvas
import requests
from PIL import Image, ImageTk
import io
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

API_KEY = "API KEY"

def download(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()  # En yüksek çözünürlüklü akışı seç
        video.download("D:/pythonMachineLearning/MüzikUygulaması")
        print(f"{yt.title} başarıyla indirildi.")
    except VideoUnavailable:
        print("Video mevcut değil.")
    except Exception as e:
        print(f"İndirme sırasında hata oluştu: {e}")

def search_youtube(query, max_results=10):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults={max_results}&key={API_KEY}"
    response = requests.get(url)
    return response.json()

search_query = "Three Days Grace Im Machine"
results = search_youtube(search_query, max_results=10)
print("API Response:", results)

root = tk.Tk()
root.title("YouTube Search Results")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = Canvas(frame)
scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

for index, item in enumerate(results["items"]):
    video_id = item["id"]["videoId"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    thumbnail_url = item["snippet"]["thumbnails"]["default"]["url"]

    response = requests.get(thumbnail_url)
    image = Image.open(io.BytesIO(response.content))
    image = image.resize((120, 90), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    img_label = tk.Label(scrollable_frame, image=photo)
    img_label.image = photo
    img_label.grid(row=index, column=0, padx=10, pady=5)

    link_button = tk.Button(
        scrollable_frame,
        text=video_url,
        fg="blue",
        cursor="hand2",
        command=lambda url=video_url: print(f"Aç: {url}"),
    )
    link_button.grid(row=index, column=1, padx=10, pady=5, sticky="w")

    download_button = tk.Button(
        scrollable_frame,
        text="Download",
        fg="black",
        cursor="hand2",
        command=lambda url=video_url: download(url)
    )
    download_button.grid(row=index, column=2, padx=10)


root.mainloop()
