import tkinter as tk
from tkinter import scrolledtext, messagebox
from transformers import pipeline

# Load summarizer pipeline once
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text():
    """
    Take text from input box, generate summary, and display in output box.
    """
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please paste some text first!")
        return

    try:
        summary = summarizer_pipeline(input_text, max_length=120, min_length=30, do_sample=False)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, summary[0]['summary_text'])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create main window
root = tk.Tk()
root.title("AI Chat Summarizer")
root.geometry("700x500")

# Input label + text box
tk.Label(root, text="Paste your text:").pack(anchor="w", padx=10, pady=5)
input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
input_box.pack(padx=10, pady=5)

# Summarize button
summarize_button = tk.Button(root, text="Summarize", command=summarize_text)
summarize_button.pack(pady=10)

# Output label + text box
tk.Label(root, text="Summary:").pack(anchor="w", padx=10, pady=5)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
output_box.pack(padx=10, pady=5)

# Run the GUI loop
root.mainloop()
