import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from transformers import pipeline
import PyPDF2

# Load summarizer pipeline once
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_with_ai(text: str) -> str:
    """Generate a summary using HuggingFace model."""
    summary = summarizer_pipeline(text, max_length=120, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def summarize_with_truncation(text: str, max_chars: int = 200) -> str:
    """Return truncated text up to max_chars characters."""
    return text[:max_chars] + ("..." if len(text) > max_chars else "")

def summarize_text():
    """Read text from input box, process based on selected mode, display output."""
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please paste or load some text first!")
        return

    try:
        if mode_var.get() == 1:
            summary = summarize_with_ai(input_text)
        else:
            summary = summarize_with_truncation(input_text)

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, summary)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_summary():
    """Save the summary text to a file."""
    summary_text = output_box.get("1.0", tk.END).strip()
    if not summary_text:
        messagebox.showwarning("Warning", "There is no summary to save!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(summary_text)
        messagebox.showinfo("Saved", f"Summary saved to {file_path}")

def load_text():
    """Load plain text from a .txt file into input box."""
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, file_content)
            messagebox.showinfo("Loaded", f"Text loaded from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")

def load_pdf():
    """Load text from a PDF file into input box."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                pdf_text = ""
                for page in reader.pages:
                    pdf_text += page.extract_text() + "\n"
            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, pdf_text)
            messagebox.showinfo("Loaded", f"PDF loaded from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load PDF: {e}")

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("AI Chat Summarizer")
root.geometry("800x650")
root.configure(bg="#1e1e1e")  # dark theme background

# Common styles
label_style = {"bg": "#1e1e1e", "fg": "white", "font": ("Arial", 12, "bold")}
text_style = {"bg": "#2d2d2d", "fg": "white", "insertbackground": "white", "font": ("Consolas", 11)}

# Input label + text box
tk.Label(root, text="Paste your text:", **label_style).pack(anchor="w", padx=10, pady=5)
input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=12, **text_style)
input_box.pack(padx=10, pady=5)

# Mode selection
mode_var = tk.IntVar(value=1)  # 1 = AI, 2 = Truncation
mode_frame = tk.Frame(root, bg="#1e1e1e")
mode_frame.pack(pady=5)
tk.Label(mode_frame, text="Choose mode:", **label_style).pack(side="left", padx=5)
tk.Radiobutton(mode_frame, text="AI summary", variable=mode_var, value=1,
               bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Arial", 11)).pack(side="left", padx=5)
tk.Radiobutton(mode_frame, text="Truncation", variable=mode_var, value=2,
               bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Arial", 11)).pack(side="left", padx=5)

# Buttons frame
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

btn_style = {"width": 15, "height": 2, "font": ("Arial", 11, "bold")}
load_button = tk.Button(button_frame, text="Load from TXT", command=load_text,
                        bg="#3a3d41", fg="white", activebackground="#2d2d2d", **btn_style)
load_button.pack(side="left", padx=15)

load_pdf_button = tk.Button(button_frame, text="Load from PDF", command=load_pdf,
                            bg="#3a3d41", fg="white", activebackground="#2d2d2d", **btn_style)
load_pdf_button.pack(side="left", padx=15)

summarize_button = tk.Button(button_frame, text="Summarize", command=summarize_text,
                             bg="#007acc", fg="white", activebackground="#005f99", **btn_style)
summarize_button.pack(side="left", padx=15)

save_button = tk.Button(button_frame, text="Save to file", command=save_summary,
                        bg="#3a3d41", fg="white", activebackground="#2d2d2d", **btn_style)
save_button.pack(side="left", padx=15)

# Output label + text box
tk.Label(root, text="Summary:", **label_style).pack(anchor="w", padx=10, pady=5)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=12, **text_style)
output_box.pack(padx=10, pady=5)

# Run the GUI loop
root.mainloop()
