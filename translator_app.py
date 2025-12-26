import tkinter as tk
from tkinter import messagebox
from googletrans import Translator
import ttkbootstrap as tb
import threading
from gtts import gTTS
import pyglet
import tempfile

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
    "German": "de",
    "Italian": "it",
    "Turkish": "tr",
    "Indian (Hindi)": "hi"
}

# -------------------- TITLE --------------------
title_frame = tk.Frame(root, bg=root.cget("background"))
tk.Label(title_frame, text="🌐 Language Translation Tool",
         font=("Segoe UI Emoji", 22, "bold"), fg="white",
         bg=root.cget("background")).pack()
tk.Label(title_frame, text="Fast • Free • Real-Time Translation",
         font=("Segoe UI", 11), fg="#cbd5e1",
         bg=root.cget("background")).pack()
title_frame.pack(pady=20)

# -------------------- MAIN FRAME --------------------
main_frame = tk.Frame(root, bg="#1e293b")
main_frame.pack(padx=20, pady=10, fill="both", expand=True)

# -------------------- LANGUAGE SELECTION --------------------
lang_frame = tk.Frame(main_frame, bg="#1e293b")
lang_frame.pack(pady=10)

source_lang = tk.StringVar(value="English")
target_lang = tk.StringVar(value="Arabic")

source_box = tb.Combobox(lang_frame, textvariable=source_lang,
                         values=list(languages.keys()), width=20,
                         bootstyle="dark", state="readonly")
source_box.grid(row=0, column=0, padx=10)

swap_btn = tb.Button(lang_frame, text="⇄", bootstyle="info", width=3)
swap_btn.grid(row=0, column=1, padx=5)

target_box = tb.Combobox(lang_frame, textvariable=target_lang,
                         values=list(languages.keys()), width=20,
                         bootstyle="dark", state="readonly")
target_box.grid(row=0, column=2, padx=10)

# -------------------- TEXT AREAS --------------------
text_frame = tk.Frame(main_frame, bg="#1e293b")
text_frame.pack(fill="both", expand=True, padx=15, pady=10)
text_frame.columnconfigure(0, weight=1)
text_frame.columnconfigure(1, weight=1)

input_frame = tk.Frame(text_frame, bg="#1e293b")
input_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))
tk.Label(input_frame, text="Enter Text", font=("Segoe UI",13,"bold"),
         bg="#1e293b", fg="white").pack(anchor="w")
input_text = tk.Text(input_frame, font=("Segoe UI",12),
                     wrap="word", bg="#0f172a", fg="white",
                     bd=0, insertbackground="white")
input_text.pack(fill="both", expand=True)

output_frame = tk.Frame(text_frame, bg="#1e293b")
output_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0))
tk.Label(output_frame, text="Translated Text", font=("Segoe UI",13,"bold"),
         bg="#1e293b", fg="white").pack(anchor="w")
output_text = tk.Text(output_frame, font=("Segoe UI",12),
                      wrap="word", bg="#0f172a", fg="white",
                      bd=0, insertbackground="white")
output_text.pack(fill="both", expand=True)

# -------------------- COPY BUTTON --------------------
def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", tk.END))
    messagebox.showinfo("Copied", "Translated text copied")

copy_btn = tk.Button(output_frame, text="📋", font=("Segoe UI Emoji",10),
                     bg="#0f172a", fg="white", bd=0, cursor="hand2",
                     command=copy_text)
copy_btn.place(relx=0.92, rely=0.9, anchor="se")

# -------------------- SPEAK BUTTON --------------------
import pyglet

def speak_text():
    text = output_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("No Text", "Nothing to speak")
        return
    lang_code = languages.get(target_lang.get(), "en")

    def tts_thread():
        try:
            tts = gTTS(text=text, lang=lang_code)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                # Load audio
                music = pyglet.media.load(fp.name, streaming=False)
                player = pyglet.media.Player()
                player.queue(music)
                player.play()
                # Schedule a timer to keep GUI responsive
                def check_play(dt):
                    if player.source and player.time < player.source.duration:
                        root.after(100, lambda: check_play(dt))
                    else:
                        player.delete()
                root.after(100, lambda: check_play(0))
        except Exception as e:
            messagebox.showerror("TTS Error", str(e))

    threading.Thread(target=tts_thread, daemon=True).start()

speak_btn = tk.Button(output_frame, text="🔊", font=("Segoe UI Emoji",10),
                      bg="#0f172a", fg="white", bd=0, cursor="hand2",
                      command=speak_text)
speak_btn.place(relx=0.86, rely=0.9, anchor="se")

# -------------------- TRANSLATION --------------------
translator = Translator()

def update_output(text):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)

def translate_bg(text, src, tgt):
    try:
        result = translator.translate(text, src=src, dest=tgt)
        root.after(0, lambda: update_output(result.text))
    except Exception:
        root.after(0, lambda: update_output("⚠️ Translation unavailable"))

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        update_output("")
        return
    src = languages[source_lang.get()]
    tgt = languages[target_lang.get()]
    threading.Thread(target=translate_bg, args=(text, src, tgt), daemon=True).start()

# -------------------- EVENTS --------------------
def on_input_change(event=None):
    input_text.edit_modified(False)
    translate_text()

input_text.bind("<<Modified>>", on_input_change)
source_box.bind("<<ComboboxSelected>>", lambda e: translate_text())
target_box.bind("<<ComboboxSelected>>", lambda e: translate_text())

# -------------------- SWAP LANGUAGES --------------------
def swap_languages():
    src_lang = source_lang.get()
    tgt_lang = target_lang.get()
    source_lang.set(tgt_lang)
    target_lang.set(src_lang)
    # Swap text content
    src_text = input_text.get("1.0", tk.END)
    tgt_text = output_text.get("1.0", tk.END)
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, tgt_text.strip())
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, src_text.strip())

swap_btn.config(command=swap_languages)

# -------------------- FOOTER --------------------
footer = tk.Label(root, text="Developed using Python & Tkinter",
                  font=("Segoe UI", 9), fg="#94a3b8",
                  bg=root.cget("background"))
footer.pack(pady=5)

# -------------------- RUN --------------------
root.mainloop()
