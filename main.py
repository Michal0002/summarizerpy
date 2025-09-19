from transformers import pipeline

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
    
    if choice == "1":
        result = summarize_with_ai(text)
    elif choice == "2":
        result = summarize_with_truncation(text)
    else:
        result = "❌ Incorrect choice"

    print("📌 Result:\n")
    print(result)

if __name__ == "__main__":
    main()