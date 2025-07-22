from llm_summarizer import LLMSummarizer

if __name__ == "__main__":
    summarizer = LLMSummarizer()
    print("Testing Ollama LLM backend (Mistral)...")
    try:
        # Test connection
        if summarizer.test_connection():
            print(" Ollama server is reachable and Mistral model is loaded.")
        else:
            print(" Ollama server is not reachable or Mistral model is not loaded.")
            exit(1)
        # Test summarization
        test_text = """
        Artificial Intelligence (AI) is a rapidly evolving field of computer science focused on building smart machines capable of performing tasks that typically require human intelligence. AI is being applied in various industries, including healthcare, finance, transportation, and more. Machine learning, a subset of AI, enables computers to learn from data and improve their performance over time without being explicitly programmed.
        """
        summary = summarizer.summarize(test_text, length="Short (100-200 words)")
        print("\n--- Summary Output ---\n")
        print(summary)
        print("\n Summarization succeeded!")
    except Exception as e:
        print(f" Error: {e}")
        exit(1) 