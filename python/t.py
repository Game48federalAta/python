import tkinter as tk
import jedi


class JediIDE:
    def __init__(self, root):
        self.root = root
        self.text = tk.Text(root, wrap="word", font=("Consolas", 12))
        self.text.pack(expand=True, fill="both")

        self.text.bind("<KeyRelease>", self.on_key_release)
        self.popup = None

    def on_key_release(self, event):
        if event.keysym == "period":  # Nokta tuşu
            self.show_suggestions()
        elif event.keysym in ("Up", "Down", "Return"):
            self.navigate_suggestions(event)
        elif event.keysym == "Escape":
            self.close_popup()
        else:
            self.close_popup()

    def show_suggestions(self):
        cursor_index = self.text.index(tk.INSERT)
        content = self.text.get("1.0", tk.END)

        # Jedi Script oluştur
        line, col = map(int, cursor_index.split("."))
        script = jedi.Script(content)
        try:
            completions = script.complete(line, col)
        except Exception:
            completions = []

        if not completions:
            self.close_popup()
            return

        self.show_popup([c.name for c in completions])

    def show_popup(self, items):
        self.close_popup()

        bbox = self.text.bbox(tk.INSERT)
        if not bbox:
            return
        x, y, width, height = bbox
        x += self.text.winfo_rootx()
        y += self.text.winfo_rooty() + height

        self.popup = tk.Toplevel(self.root)
        self.popup.wm_overrideredirect(True)
        self.popup.geometry(f"+{x}+{y}")

        self.listbox = tk.Listbox(self.popup, height=8, width=30)
        for item in items:
            self.listbox.insert(tk.END, item)
        self.listbox.pack()
        self.listbox.focus_set()
        self.listbox.selection_set(0)

    def close_popup(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None

    def navigate_suggestions(self, event):
        if not self.popup:
            return

        index = self.listbox.curselection()
        if not index:
            index = [0]
        index = index[0]

        if event.keysym == "Down":
            if index < self.listbox.size() - 1:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(index + 1)
        elif event.keysym == "Up":
            if index > 0:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(index - 1)
        elif event.keysym == "Return":
            self.insert_completion()

    def insert_completion(self):
        if not self.popup:
            return
        selection = self.listbox.get(self.listbox.curselection())
        self.text.insert(tk.INSERT, selection)
        self.close_popup()


root = tk.Tk()
root.title("Jedi IDE - Mini Python Autocomplete")
app = JediIDE(root)
root.mainloop()
