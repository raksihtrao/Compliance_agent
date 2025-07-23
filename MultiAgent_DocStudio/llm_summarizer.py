import os
from typing import Optional, List
import openai

# Try to import Gemini (google-generativeai)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class LLMSummarizer:
    def __init__(self, provider: str = "openai", model: str = "gpt-3.5-turbo", openai_api_key: Optional[str] = None):
        self.provider = provider
        self.model = model
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.provider == "openai":
            self.client = openai.OpenAI(api_key=self.api_key)
        elif self.provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise ImportError("google-generativeai is not installed. Please install it to use Gemini.")
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY not set in environment.")
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def set_api_key(self, api_key: str):
        if self.provider == "openai":
            self.api_key = api_key
            self.client = openai.OpenAI(api_key=api_key)
        elif self.provider == "gemini":
            self.gemini_api_key = api_key
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel("gemini-2.5-flash")

    def summarize(self, text: str, model: Optional[str] = None, length: str = "Medium (200-400 words)") -> Optional[str]:
        if not text or len(text.strip()) == 0:
            raise Exception("No text provided for summarization.")
        word_limits = {
            "Short (100-200 words)": (100, 200),
            "Medium (200-400 words)": (200, 400),
            "Long (400-600 words)": (400, 600)
        }
        min_words, max_words = word_limits.get(length, (200, 400))
        prompt = self._create_summary_prompt(text, min_words, max_words)
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=model or self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024,
                    temperature=0.5
                )
                summary = response.choices[0].message.content.strip()
            elif self.provider == "gemini":
                response = self.gemini_model.generate_content(prompt)
                summary = response.text.strip() if response.text else ""
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            if not summary:
                raise Exception("No summary returned ")
            return summary
        except Exception as e:
            raise Exception(f"{self.provider.capitalize()} error: {str(e)}")

    def key_takeaways(self, text: str) -> List[str]:
        if not text or len(text.strip()) == 0:
            raise Exception("No text provided for key takeaways.")
        prompt = (
            "List the 5 most important, precise, and meaningful key takeaways from the following text. "
            "Each takeaway should be a single line. Do not exceed 5 lines. Be clear and specific.\n\n"
            f"Text to analyze:\n{text[:8000]}\n\nKey takeaways (one per line):"
        )
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=512,
                    temperature=0.5
                )
                takeaways_text = response.choices[0].message.content.strip()
            elif self.provider == "gemini":
                response = self.gemini_model.generate_content(prompt)
                takeaways_text = response.text.strip() if response.text else ""
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            lines = [line.lstrip('-•0123456789. ').strip() for line in takeaways_text.splitlines() if line.strip()]
            return lines[:5]
        except Exception as e:
            raise Exception(f"{self.provider.capitalize()} error (key takeaways): {str(e)}")

    def _create_summary_prompt(self, text: str, min_words: int, max_words: int) -> str:
        prompt = f"""
Please provide a comprehensive summary of the following text. The summary should:
1. Capture the main ideas and key points
2. Maintain the original meaning and context
3. Be well-structured and easy to read
4. Be between {min_words} and {max_words} words
5. Focus on the most important information
6. Use clear, professional language

Text to summarize:
{text[:8000]}

Please provide the summary:
"""
        return prompt

    def get_available_models(self) -> list:
        if self.provider == "openai":
            return [self.model]
        elif self.provider == "gemini":
            return [self.model]
        return [self.model]

    def test_connection(self) -> bool:
        try:
            prompt = "Hello!"
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=10
                )
                return True
            elif self.provider == "gemini":
                response = self.gemini_model.generate_content(prompt)
                return bool(response.text.strip()) if response.text else False
            else:
                return False
        except Exception:
            return False

    def estimate_cost(self, text: str, model: Optional[str] = None) -> dict:
        word_count = len(text.split())
        return {
            "input_tokens": word_count,
            "output_tokens": 200,
            "total_tokens": word_count + 200,
            "estimated_cost_usd": 0.0
        }

    def generate(self, prompt: str) -> str:
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024,
                    temperature=0.5
                )
                return response.choices[0].message.content.strip()
            elif self.provider == "gemini":
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip() if response.text else ""
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
        except Exception as e:
            raise Exception(f"{self.provider.capitalize()} error (generate): {str(e)}") 