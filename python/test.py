import customtkinter as ctk
from tkinter import Menu, filedialog, ttk
import tkinter as tk
import re
import io
import sys
import os


class IDE:
    def __init__(self):
        self.open_files = {}  # {file_path: {"content": str, "modified": bool}}
        self.current_file = None
        self.project_folder = None

        ctk.set_appearance_mode("dark")
        self.window = ctk.CTk()
        self.window.title("Python IDE")
        self.window.geometry("1400x800")
        self.window.resizable(True, True)

        # Menu Bar
        self.create_menu()

        # Main container
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # SIDEBAR - Sol Panel
        self.sidebar = ctk.CTkFrame(main_container, width=250, fg_color="#252526")
        self.sidebar.pack(side="left", fill="y", padx=(0, 5))
        self.sidebar.pack_propagate(False)

        # Sidebar başlık
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="EXPLORER",
            font=("Segoe UI", 12, "bold"),
            text_color="#CCCCCC",
        )
        sidebar_title.pack(pady=(10, 5), padx=10, anchor="w")

        # Proje klasörü aç butonu
        open_folder_btn = ctk.CTkButton(
            self.sidebar,
            text="📁 Open Folder",
            command=self.open_folder,
            fg_color="#007ACC",
            hover_color="#005A9E",
            height=35,
        )
        open_folder_btn.pack(pady=5, padx=10, fill="x")

        # Dosya ağacı için frame
        tree_frame = ctk.CTkFrame(self.sidebar, fg_color="#1E1E1E")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # TreeView için stil
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1E1E1E",
            foreground="white",
            fieldbackground="#1E1E1E",
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#094771")])

        # Scrollbar
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")

        # TreeView
        self.file_tree = ttk.Treeview(
            tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse"
        )
        self.file_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.config(command=self.file_tree.yview)

        # TreeView başlık gizle
        self.file_tree["show"] = "tree"

        # Dosya tıklama eventi
        self.file_tree.bind("<Double-1>", self.on_file_select)

        # SAĞ TARAF - Editor bölgesi
        editor_container = ctk.CTkFrame(main_container, fg_color="transparent")
        editor_container.pack(side="left", fill="both", expand=True)

        # SEKMELER (Tabs)
        self.tab_frame = ctk.CTkFrame(editor_container, height=35, fg_color="#2D2D30")
        self.tab_frame.pack(fill="x", pady=(0, 2))
        self.tab_frame.pack_propagate(False)

        self.tabs = {}  # {file_path: tab_button}

        # Editor alanı
        self.text_box = ctk.CTkTextbox(
            editor_container,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#1E1E1E",
            text_color="#D4D4D4",
            border_width=0,
            wrap="none",
        )
        self.text_box.pack(fill="both", expand=True)

        # Karşılama mesajı
        self.text_box.insert(
            "1.0", "# Python IDE\n# Open a folder or file to start coding..."
        )
        self.text_box.configure(state="disabled")

        # TERMINAL
        terminal_container = ctk.CTkFrame(self.window, fg_color="#1E1E1E")
        terminal_container.pack(side="bottom", fill="x", padx=5, pady=(0, 5))

        terminal_label = ctk.CTkLabel(
            terminal_container,
            text="TERMINAL",
            font=("Segoe UI", 10, "bold"),
            text_color="#CCCCCC",
        )
        terminal_label.pack(anchor="w", padx=10, pady=(5, 0))

        self.terminal_box = ctk.CTkTextbox(
            terminal_container,
            font=("Consolas", 11),
            fg_color="#1E1E1E",
            text_color="#CCCCCC",
            height=150,
        )
        self.terminal_box.pack(fill="both", padx=5, pady=5)

        # Keybindings
        self.text_box.bind("<KeyRelease>", self.on_text_change)
        self.window.bind("<F5>", self.run_code)
        self.window.bind("<Control-s>", self.save_current_file)
        self.window.bind("<Control-w>", self.close_current_tab)

    def create_menu(self):
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        # File Menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label="Open File", command=self.open_file, accelerator="Ctrl+O"
        )
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(
            label="Save", command=self.save_current_file, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Close Tab", command=self.close_current_tab, accelerator="Ctrl+W"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Run Menu
        run_menu = Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run Code", command=self.run_code, accelerator="F5")
        menu_bar.add_cascade(label="Run", menu=run_menu)

    def open_folder(self):
        folder = filedialog.askdirectory(title="Select Project Folder")
        if folder:
            self.project_folder = folder
            self.populate_tree(folder)

    def populate_tree(self, folder):
        # TreeView'i temizle
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        # Klasör adını root olarak ekle
        folder_name = os.path.basename(folder)
        root_node = self.file_tree.insert(
            "", "end", text=f"📁 {folder_name}", values=[folder]
        )

        # Alt klasör ve dosyaları ekle
        self.add_tree_nodes(root_node, folder)
        self.file_tree.item(root_node, open=True)

    def add_tree_nodes(self, parent, path):
        try:
            items = sorted(os.listdir(path))
            # Önce klasörler, sonra dosyalar
            folders = [
                item for item in items if os.path.isdir(os.path.join(path, item))
            ]
            files = [item for item in items if os.path.isfile(os.path.join(path, item))]

            for folder in folders:
                if folder.startswith("."):  # Gizli klasörleri atla
                    continue
                full_path = os.path.join(path, folder)
                node = self.file_tree.insert(
                    parent, "end", text=f"📁 {folder}", values=[full_path]
                )
                # Alt klasörleri ekle
                self.add_tree_nodes(node, full_path)

            for file in files:
                if file.startswith("."):  # Gizli dosyaları atla
                    continue
                full_path = os.path.join(path, file)
                # Dosya uzantısına göre emoji
                icon = "🐍" if file.endswith(".py") else "📄"
                self.file_tree.insert(
                    parent, "end", text=f"{icon} {file}", values=[full_path]
                )
        except PermissionError:
            pass

    def on_file_select(self, event):
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            file_path = self.file_tree.item(item)["values"]
            if file_path and os.path.isfile(file_path[0]):
                self.open_file_in_editor(file_path[0])

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        if file_path:
            self.open_file_in_editor(file_path)

    def open_file_in_editor(self, file_path):
        # Dosya zaten açıksa, o sekmeye geç
        if file_path in self.open_files:
            self.switch_to_file(file_path)
            return

        # Dosyayı oku
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.terminal_box.delete("1.0", "end")
            self.terminal_box.insert("1.0", f"Error opening file: {e}")
            return

        # Dosyayı kaydet
        self.open_files[file_path] = {"content": content, "modified": False}

        # Sekme oluştur
        self.create_tab(file_path)

        # Dosyayı göster
        self.switch_to_file(file_path)

    def create_tab(self, file_path):
        file_name = os.path.basename(file_path)

        # Tab butonu
        tab_btn = ctk.CTkButton(
            self.tab_frame,
            text=f"  {file_name}  ",
            command=lambda: self.switch_to_file(file_path),
            fg_color="#2D2D30",
            hover_color="#1E1E1E",
            text_color="white",
            height=30,
            corner_radius=0,
        )
        tab_btn.pack(side="left", padx=1)

        # Kapat butonu
        close_btn = ctk.CTkButton(
            tab_btn,
            text="✕",
            width=20,
            height=20,
            command=lambda: self.close_tab(file_path),
            fg_color="transparent",
            hover_color="#E81123",
            text_color="#CCCCCC",
        )
        close_btn.place(relx=1, rely=0.5, anchor="e", x=-5)

        self.tabs[file_path] = tab_btn

    def switch_to_file(self, file_path):
        if file_path not in self.open_files:
            return

        # Mevcut dosyayı kaydet
        if self.current_file and self.current_file in self.open_files:
            self.open_files[self.current_file]["content"] = self.text_box.get(
                "1.0", "end-1c"
            )

        # Yeni dosyayı yükle
        self.current_file = file_path
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", self.open_files[file_path]["content"])

        # Syntax highlighting
        self.highlight_syntax()

        # Aktif sekmeyi vurgula
        for path, tab in self.tabs.items():
            if path == file_path:
                tab.configure(fg_color="#1E1E1E")
            else:
                tab.configure(fg_color="#2D2D30")

        # Pencere başlığını güncelle
        self.window.title(f"Python IDE - {os.path.basename(file_path)}")

    def close_tab(self, file_path):
        if file_path in self.open_files:
            # Değişiklik varsa uyar
            if self.open_files[file_path]["modified"]:
                # Burada gerçek uygulamada bir dialog gösterilmeli
                pass

            # Sekmeyi kaldır
            if file_path in self.tabs:
                self.tabs[file_path].destroy()
                del self.tabs[file_path]

            # Dosyayı kapat
            del self.open_files[file_path]

            # Başka dosya varsa ona geç
            if self.open_files:
                self.switch_to_file(list(self.open_files.keys())[0])
            else:
                self.current_file = None
                self.text_box.delete("1.0", "end")
                self.text_box.insert("1.0", "# No file open")
                self.text_box.configure(state="disabled")
                self.window.title("Python IDE")

    def close_current_tab(self, event=None):
        if self.current_file:
            self.close_tab(self.current_file)

    def save_current_file(self, event=None):
        if not self.current_file:
            return

        try:
            content = self.text_box.get("1.0", "end-1c")
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)

            self.open_files[self.current_file]["content"] = content
            self.open_files[self.current_file]["modified"] = False

            # Sekme başlığını güncelle (yıldızı kaldır)
            file_name = os.path.basename(self.current_file)
            self.tabs[self.current_file].configure(text=f"  {file_name}  ")

            self.terminal_box.delete("1.0", "end")
            self.terminal_box.insert("1.0", f"✓ Saved: {self.current_file}")
        except Exception as e:
            self.terminal_box.delete("1.0", "end")
            self.terminal_box.insert("1.0", f"Error saving file: {e}")

    def on_text_change(self, event=None):
        if self.current_file and self.current_file in self.open_files:
            current_content = self.text_box.get("1.0", "end-1c")
            saved_content = self.open_files[self.current_file]["content"]

            # Değişiklik varsa işaretle
            if current_content != saved_content:
                if not self.open_files[self.current_file]["modified"]:
                    self.open_files[self.current_file]["modified"] = True
                    file_name = os.path.basename(self.current_file)
                    self.tabs[self.current_file].configure(text=f"  ● {file_name}  ")

            self.highlight_syntax()

    def highlight_syntax(self):
        # Tag'leri tanımla
        self.text_box.tag_config("keyword", foreground="#569CD6")
        self.text_box.tag_config("string", foreground="#CE9178")
        self.text_box.tag_config("comment", foreground="#6A9955")
        self.text_box.tag_config("number", foreground="#B5CEA8")
        self.text_box.tag_config("function", foreground="#DCDCAA")
        self.text_box.tag_config("builtin", foreground="#4EC9B0")

        # Eski tag'leri temizle
        for tag in ["keyword", "string", "comment", "number", "function", "builtin"]:
            self.text_box.tag_remove(tag, "1.0", "end")

        content = self.text_box.get("1.0", "end-1c")

        # Yorumlar
        for match in re.finditer(r"#[^\n]*", content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_box.tag_add("comment", start, end)

        # String'ler
        for match in re.finditer(r'["\'][^"\']*["\']', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_box.tag_add("string", start, end)

        # Sayılar
        for match in re.finditer(r"\b\d+\b", content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_box.tag_add("number", start, end)

        # Fonksiyon isimleri
        for match in re.finditer(r"def\s+(\w+)", content):
            start = f"1.0+{match.start(1)}c"
            end = f"1.0+{match.end(1)}c"
            self.text_box.tag_add("function", start, end)

        # Built-in fonksiyonlar
        builtins = [
            "print",
            "len",
            "range",
            "str",
            "int",
            "list",
            "dict",
            "open",
            "input",
        ]
        for builtin in builtins:
            for match in re.finditer(rf"\b{builtin}\b", content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_box.tag_add("builtin", start, end)

        # Keywords
        keywords = [
            "def",
            "class",
            "if",
            "elif",
            "else",
            "for",
            "while",
            "return",
            "import",
            "from",
            "as",
            "try",
            "except",
            "with",
            "pass",
            "break",
            "continue",
            "True",
            "False",
            "None",
            "and",
            "or",
            "not",
            "in",
            "is",
            "lambda",
        ]
        for keyword in keywords:
            for match in re.finditer(rf"\b{keyword}\b", content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_box.tag_add("keyword", start, end)

    def run_code(self, event=None):
        if not self.current_file:
            self.terminal_box.delete("1.0", "end")
            self.terminal_box.insert("1.0", "No file to run!")
            return

        # Stdout ve stderr'i yakala
        buffer = io.StringIO()
        sys.stdout = buffer
        sys.stderr = buffer

        try:
            code = self.text_box.get("1.0", "end-1c")
            exec(code)
        except Exception as e:
            print(f"Error: {e}")

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        # Terminal'i güncelle
        self.terminal_box.delete("1.0", "end")
        output = buffer.getvalue()
        if output:
            self.terminal_box.insert("1.0", output)
        else:
            self.terminal_box.insert("1.0", "✓ Code executed successfully (no output)")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    ide = IDE()
    ide.run()
