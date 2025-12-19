import tkinter as tk
from tkinter import messagebox
import urllib.request, urllib.parse, json
import ttkbootstrap as tb

# -------------------- MAIN WINDOW --------------------
root = tb.Window(themename="darkly")
root.title("🌐 Language Translation Tool")
root.geometry("900x600")
root.resizable(True, True)

# -------------------- LANGUAGES --------------------
languages = {
    "English": "en",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Turkish": "tr"
}

# -------------------- TITLE --------------------
title_frame = tk.Frame(root, bg=root.cget("background"))
tk.Label(title_frame, text="🌐 Language Translation Tool",
         font=("Segoe UI Emoji", 22, "bold"), fg="white", bg=root.cget("background")).pack()
tk.Label(title_frame, text="Fast • Free • Real-Time Translation",
         font=("Segoe UI", 11), fg="#cbd5e1", bg=root.cget("background")).pack()
title_frame.pack(pady=20)

# -------------------- MAIN FRAME --------------------
main_frame = tk.Frame(root, bg="#1e293b", bd=0)
main_frame.pack(padx=20, pady=10, fill="both", expand=True)

# -------------------- LANGUAGE SELECTION --------------------
lang_frame = tk.Frame(main_frame, bg="#1e293b")
lang_frame.pack(pady=10)

source_lang = tk.StringVar(value="English")
target_lang = tk.StringVar(value="Arabic")

source_box = tb.Combobox(lang_frame, textvariable=source_lang, values=list(languages.keys()),
                         width=18, bootstyle="dark", state="readonly")
source_box.grid(row=0, column=0, padx=10)

swap_btn = tb.Button(lang_frame, text="⇄", bootstyle="info", width=3)
swap_btn.grid(row=0, column=1, padx=5)

target_box = tb.Combobox(lang_frame, textvariable=target_lang, values=list(languages.keys()),
                         width=18, bootstyle="dark", state="readonly")
target_box.grid(row=0, column=2, padx=10)

def swap_languages():
    src, tgt = source_lang.get(), target_lang.get()
    source_lang.set(tgt)
    target_lang.set(src)

swap_btn.configure(command=swap_languages)

# -------------------- TEXT BOXES FRAME --------------------
text_frame = tk.Frame(main_frame, bg="#1e293b")
text_frame.pack(fill="both", expand=True, padx=15, pady=10)

text_frame.columnconfigure(0, weight=1)
text_frame.columnconfigure(1, weight=1)
text_frame.rowconfigure(0, weight=1)

# -------------------- INPUT TEXT --------------------
input_frame = tk.Frame(text_frame, bg="#1e293b")
input_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))

tk.Label(input_frame, text="Enter Text", font=("Segoe UI", 13, "bold"),
         bg="#1e293b", fg="white").pack(anchor="w", pady=(0,5))

input_text = tk.Text(input_frame, font=("Segoe UI", 12), wrap="word",
                     bg="#0f172a", fg="white", height=10, bd=0, insertbackground="white")
input_text.pack(fill="both", expand=True)

# -------------------- OUTPUT TEXT --------------------
output_frame = tk.Frame(text_frame, bg="#1e293b")
output_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0))

tk.Label(output_frame, text="Translated Text", font=("Segoe UI", 13, "bold"),
         bg="#1e293b", fg="white").pack(anchor="w", pady=(0,5))

output_text = tk.Text(output_frame, font=("Segoe UI", 12), wrap="word",
                      bg="#0f172a", fg="white", height=10, bd=0, insertbackground="white")
output_text.pack(fill="both", expand=True)

# -------------------- COPY BUTTON OVERLAY --------------------
def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", tk.END))
    messagebox.showinfo("Copied", "Translated text copied to clipboard")

# Create a small emoji button overlay
copy_btn = tk.Button(output_frame, text="📋", font=("Segoe UI Emoji", 10),
                     bd=0, bg="#0f172a", fg="white", activebackground="#0f172a",
                     activeforeground="white", cursor="hand2", command=copy_text)

# Place button at bottom-right corner inside the text box
def place_copy_btn(event=None):
    x = output_text.winfo_width() - 50
    y = output_text.winfo_height() - 25
    copy_btn.place(x=x, y=y)

output_text.bind("<Configure>", place_copy_btn)
place_copy_btn()  # initial placement

# -------------------- AUTOMATIC TRANSLATION --------------------
def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        output_text.delete("1.0", tk.END)
        return
    src = languages[source_lang.get()]
    tgt = languages[target_lang.get()]
    try:
        url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode({
            "q": text, "langpair": f"{src}|{tgt}"
        })
        with urllib.request.urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode())
        translated = data["responseData"]["translatedText"]
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")

def on_input_change(event=None):
    input_text.edit_modified(False)
    if hasattr(on_input_change, "after_id"):
        root.after_cancel(on_input_change.after_id)
    on_input_change.after_id = root.after(500, translate_text)

input_text.bind("<<Modified>>", on_input_change)

# -------------------- FOOTER --------------------
footer = tk.Label(root, text="Developed using Python & Tkinter",
                  font=("Segoe UI", 9), bg=root.cget("background"), fg="#94a3b8")
footer.pack(pady=5)

# -------------------- RUN --------------------
root.mainloop()
