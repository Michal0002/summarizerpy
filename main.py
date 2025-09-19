from transformers import pipeline

def main():
    print("=== AI Chat Summarizer ===")

    text = input("👉 Paste text into summary: ")

    print("\n Generating summary...\n")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    summary = summarizer(text, max_length=120, min_length=30, do_sample=False)

    print("📌 Result:\n")
    print(summary[0]['summary_text'])
    
if __name__ == "__main__":
    main()