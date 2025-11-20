import tkinter as tk
from tkinter import ttk
from collections import defaultdict
from nltk import bigrams
from textblob import TextBlob
import random

def build_ngram_model(sentences):
    model = defaultdict(list)
    for sentence in sentences:
        for w1, w2 in bigrams(sentence, pad_right=True, pad_left=True):
            model[w1].append(w2)
    return model

def autocorrect_text(text):
    blob = TextBlob(text)
    return str(blob.correct())

def predict_next_words(word, count=3):
    possible_words = model.get(word, None)
    if not possible_words:

        return random.sample(list(model.keys()), min(count, len(model)))

    unique_words = list(set(possible_words))
    sorted_words = sorted(unique_words, key=lambda w: possible_words.count(w), reverse=True)

    suggestions = sorted_words[:count]
    if len(suggestions) < count:
        suggestions += random.sample(list(model.keys()), count - len(suggestions))
    return suggestions
def update_prediction(event=None):
    user_text = input_box.get("1.0", tk.END).strip()

    if not user_text:
        corrected_label.config(text="Autocorrected: ")
        suggestion_label.config(text="Next word suggestions:")
        for btn in suggestion_buttons:
            btn.config(text="", state="disabled")
        return

    corrected = autocorrect_text(user_text)
    corrected_label.config(text=f"Autocorrected: {corrected}")

    words = corrected.split()
    if len(words) == 0:
        suggestion_label.config(text="Next word suggestions:")
        return
    next_words = predict_next_words(words[-1])
    suggestion_label.config(text=f"Next word suggestions:")

    for i, btn in enumerate(suggestion_buttons):
        if i < len(next_words):
            btn.config(text=next_words[i], state="normal")
        else:
            btn.config(text="", state="disabled")


def insert_suggestion(word):
    current_text = input_box.get("1.0", tk.END).strip()
    if not current_text.endswith(" "):
        current_text += " "
    input_box.delete("1.0", tk.END)
    input_box.insert(tk.END, current_text + word + " ")
    update_prediction()


sentences = [
    "I love machine learning".split(),
    "machine learning is fun".split(),
    "deep learning improves predictions".split(),
    "I enjoy learning new things".split(),
    "Python makes machine learning easy".split(),
    "AI and data science are powerful".split(),
    "learning artificial intelligence is exciting".split()
]

model = build_ngram_model(sentences)

root = tk.Tk()
root.title("AI Keyboard (Autocorrect + Prediction)")
root.geometry("600x400")
root.configure(bg="#466bd1")

title_label = ttk.Label(root, text="AI Smart Keyboard", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

input_box = tk.Text(root, height=5, width=60, font=("Arial", 12))
input_box.pack(pady=10)
input_box.bind("<KeyRelease>", update_prediction)

corrected_label = ttk.Label(root, text="Autocorrected: ", font=("Arial", 11))
corrected_label.pack(pady=5)

suggestion_label = ttk.Label(root, text="Next word suggestions:", font=("Arial", 11, "italic"))
suggestion_label.pack(pady=5)

frame = ttk.Frame(root)
frame.pack(pady=10)

suggestion_buttons = []
for i in range(3):
    btn = ttk.Button(
        frame,
        text="",
        width=20,
        command=lambda b=i: insert_suggestion(suggestion_buttons[b].cget("text"))
    )
    btn.grid(row=0, column=i, padx=5)
    suggestion_buttons.append(btn)

update_prediction()

root.mainloop()