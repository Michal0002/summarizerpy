from transformers import pipeline
import tkinter as tk
from tkinter import scrolledtext, messagebox

summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_with_ai(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=120, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def summarize_with_truncation(text, max_chars=200):
    return text[:max_chars] + ("..." if len(text) > max_chars else "")    
def main():
    print("=== AI Chat Summarizer ===")
    text = input("👉 Paste text into summary: ")

    print("\nChoose the mode of operation:")
    print("1 - AI summary (HuggingFace)")
    print("2 - Simple truncation (truncation)")
    choice = input("Your choice (1/2): ")

    print("\n🔄 Processing... \n")
    
    try:
        if choice == "1":
            result = summarize_with_ai(text)
        elif choice == "2":
            result = summarize_with_truncation(text)
        else:
            result = "❌ Incorrect choice"
    except Exception as e:
        result = f"An error occurred: {e}"

    print("📌 Result:\n")
    print(result)

    save = input("\n Do you want to save the result to a file? (y/n): ")

    if save.lower() == "y":
        with open("summary.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("💾 Saved to summary.txt")

if __name__ == "__main__":
    main()
