import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import requests
from PIL import Image, ImageTk
import io
import yt_dlp

API_KEY = "API_key"


filepath = ""
dir_ = ""
dirname = ""
file_name = ""


music_name = ""

canvas = None
scroll_bar = None
scrollable_frame = None
search_bar = None
pygame.mixer.init()


def show_playlist_music(path):
    list_box_playlist.delete(0, tk.END)  # Önceki öğeleri temizle
    for file in os.listdir(path):
        if file.endswith(".mp3"):  # Sadece müzik dosyalarını al
            list_box_playlist.insert(tk.END, file)


def create_playlist():
    global img_json
    folder_path = "icon"

    if not os.path.exists(folder_path):  # Klasör yoksa oluştur
        os.makedirs(folder_path)
        print("Klasör oluşturuldu!")
    else:
        print("Klasör zaten var!")


def get_index_file(file_path: str):
    global dirname
    file_name = os.path.basename(file_path)  # Dosya adını al
    if file_name in dir_:  # Dosya adı dir_ listesinde varsa
        return dir_.index(file_name)
    return -1  # Eğer bulunamazsa, -1 döner


def del_trash_file(list_dir, filetype):
    result = []

    for x in list_dir:
        if x.endswith(filetype):
            result.append(x)
    return result


def play_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    song_name_label


def open_music():
    global filepath, dir_, dirname, file_name, song_name_label

    filepath = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if filepath:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        dirname = os.path.dirname(filepath)
        dir_ = del_trash_file(os.listdir(dirname), ".mp3")
        file_name = os.path.basename(filepath)
        song_name_label = tk.Label(frame1, text="Çalan Şarkı: " + file_name)
        song_name_label.place(x=300, y=300)
        create_playlist()
        show_playlist_music(dirname)
        show_thumbail(file_name,dirname)


def pause_music(event=None):
    pygame.mixer.music.pause()


def continue_music(event=None):
    pygame.mixer.music.unpause()


def set_volume(variable):
    pygame.mixer.music.set_volume(int(variable) / 100)


def show_thumbail(song_name,dirname):
    image = Image.open(dirname+"/icon/"+song_name.replace(".mp3","")+".png")
    image = image.resize((600, 280), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    label=tk.Label(frame1,image=photo).place(x=250,y=0)
    label.image=photo

def back_song():
    global filepath, dirname, file_name, song_name_label
    index = get_index_file(filepath)
    pygame.mixer.music.load(dirname + "/" + dir_[index - 1])
    pygame.mixer.music.play()
    file_name = dir_[index - 1]
    song_name_label.configure(text=f"Çalan Şarkı:" + file_name)
    filepath = dirname + "/" + file_name
    show_thumbail(file_name,dirname)


def next_song():
    global filepath, dirname, file_name, song_name_label
    index = get_index_file(filepath)
    try:
        pygame.mixer.music.load(dirname + "/" + dir_[index + 1])
        pygame.mixer.music.play()
        file_name = dir_[index + 1]
        song_name_label.configure(text=f"Çalan Şarkı: " + file_name)
        filepath = dirname + "/" + file_name
        show_thumbail(file_name,dirname)
    except IndexError:
        index = -1
        pygame.mixer.music.load(dirname + "/" + dir_[index+1])
        pygame.mixer.music.play()
        file_name = dir_[index+1]
        song_name_label.configure(text=f"Çalan Şarkı: " + file_name)
        filepath = dirname + "/" + file_name
        show_thumbail(file_name,dirname)


def set_position_music(variable):
    pos = float(variable)
    pygame.mixer.music.set_pos(pos)


def search_youtube(query, max_results=10):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults={max_results}&key={API_KEY}"
    response = requests.get(url)
    return response.json()


def del_search_result():
    global canvas, scroll_bar, scrollable_frame
    if canvas:
        canvas.destroy()
    if scroll_bar:
        scroll_bar.destroy()
    if scrollable_frame:
        scrollable_frame.destroy()


def download(url):
    global dirname
    # İndirme seçeneklerini ayarlama
    ydl_opts = {
        "format": "bestaudio/best",  # En iyi ses kalitesini seç
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Ses dosyasını MP3'e dönüştür
                "preferredcodec": "mp3",  # MP3 formatı
                "preferredquality": "192",  # Ses kalitesi
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    if dirname != "":
        create_playlist()
        download_thumbnail(url=url, save_path="./icon/" + filename.replace(".webm","")+ ".png")
    else:
        download_thumbnail(url=url, save_path="./icon/" + filename.replace(".webm","")+ ".png")
    # yt-dlp ile indirme işlemi"""


def download_thumbnail(url, save_path):
    try:
        # Video ID'sini URL'den çıkarma
        video_id = url.split("v=")[-1]

        # Thumbnail URL'leri için farklı formatlar
        thumbnail_urls = [
            f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            f"https://i.ytimg.com/vi/{video_id}/hq720.jpg",
            f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
        ]

        # Thumbnail URL'lerini sırayla test et
        for thumbnail_url in thumbnail_urls:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                print(f"Thumbnail başarıyla bulundu: {thumbnail_url}")
                # Thumbnail'ı kaydetme
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"Thumbnail başarıyla indirildi: {save_path}")
                break  # Thumbnail bulunduğu anda döngüden çık
        else:
            print("Thumbnail indirilemedi.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")


def get_search_bar_text():
    global music_name, canvas, scrollable_frame, scroll_bar, dirname
    music_name = search_bar.get()

    results = search_youtube(music_name)

    canvas = tk.Canvas(search_frame)
    scroll_bar = tk.Scrollbar(search_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_bar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

    result_label = tk.Label(scrollable_frame, text="Search Result:")
    result_label.place(x=250, y=10)

    delete_search_result_button = tk.Button(
        search_frame, text="Delete Result", command=del_search_result
    )
    delete_search_result_button.place(x=700, y=10)

    for index, item in enumerate(results["items"]):
        # videoId anahtarının mevcut olup olmadığını kontrol et
        if "videoId" in item["id"]:
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
                command=lambda url=video_url: download(url=url),
            )
            download_button.grid(row=index, column=2, padx=10)
        else:
            print(f"Video ID bulunamadı: {item['id']}")


def open_selected_music_in_playlist(event):
    global dirname, song_name_label
    selected_index = list_box_playlist.curselection()  # Seçili öğenin indexini al
    if selected_index:  # Eğer bir öğe seçildiyse
        selected_song = list_box_playlist.get(
            selected_index[0]
        )  # Seçilen müziğin adını al
        play_music(dirname + "/" + selected_song)
        song_name_label.configure(text="Çalan Şarkı: " + selected_song)
        show_thumbail(selected_song,dirname)


def re_load_page(event):
    global dirname
    if notebook.index(notebook.select())==0:
        list_box_playlist = tk.Listbox(frame1, width=40, height=100)
        list_box_playlist.place(x=0, y=0)

        list_box_playlist.delete(0, tk.END)  # Önceki öğeleri temizle
        for file in os.listdir(dirname):
            if file.endswith(".mp3"):  # Sadece müzik dosyalarını al
                list_box_playlist.insert(tk.END, file)


root = tk.Tk()
root.geometry("800x500")
root.title("Müzik Çalar")


# Notebook (Sekme yapısı)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# 1. Sekme (Ana Sayfa)
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Ana Sayfa")

song_name_label = tk.Label(frame1, text="Şarkı çalmıyor").place(x=300, y=300)

# 2.sekme Arama sekmesi
search_frame = ttk.Frame(notebook)
notebook.add(search_frame, text="Arama")

search_bar = tk.Entry(search_frame)
search_bar.place(x=300, y=0)


search_button = tk.Button(
    search_frame, text="Ara", command=get_search_bar_text, width=5, height=1
).place(x=420, y=0)

sound_level = tk.Scale(
    frame1,
    from_=0,
    to=100,
    orient="horizontal",
    label="Ses seviyesi",
    command=set_volume,
    length=100,
)
sound_level.set(50)
sound_level.place(x=350, y=400)


play_button = tk.Button(frame1, text="Oynat", command=continue_music)
play_button.place(x=350, y=350)

play_button = tk.Button(frame1, text="Durdur", command=pause_music)
play_button.place(x=395, y=350)

play_button = tk.Button(frame1, text="Önceki", command=back_song)
play_button.place(x=300, y=350)

play_button = tk.Button(frame1, text="Sonraki", command=next_song)
play_button.place(x=450, y=350)


menu_bar = tk.Menu(root)

# "File" Menüsü
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Aç", command=open_music)
file_menu.add_separator()
file_menu.add_command(label="Çıkış", command=root.quit)


playlist_menu = tk.Menu(menu_bar, tearoff=0)
playlist_menu.add_command(label="Create New Playlist")
playlist_menu.add_command(label="Delete Playlist")
playlist_menu.add_command(label="Show Playlist")


memory_menu = tk.Menu(menu_bar, tearoff=0)
memory_menu.add_command(label="Show")

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Playlist", menu=playlist_menu)
menu_bar.add_cascade(label="Memory", menu=memory_menu)

# Menü çubuğunu pencereye ekle

# Listbox oluştur
list_box_playlist = tk.Listbox(frame1, width=40, height=100)
list_box_playlist.place(x=0, y=0)

root.bind("<<ListboxSelect>>", open_selected_music_in_playlist)
root.bind("<F5>",re_load_page)
root.bind("<space>",pause_music)
root.bind("<Enter>",continue_music)

root.config(menu=menu_bar)
root.mainloop()


print(dirname)
print(filepath)

