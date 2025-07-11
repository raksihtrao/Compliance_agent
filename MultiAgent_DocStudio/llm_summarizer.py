import os
from typing import Optional, List
import openai

class LLMSummarizer:
    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        openai.api_key = self.api_key

    def set_api_key(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

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
            response = openai.ChatCompletion.create(
                model=model or self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.5
            )
            summary = response.choices[0].message["content"].strip()
            if not summary:
                raise Exception("No summary returned ")
            return summary
        except Exception as e:
            raise Exception(f"OpenAI error: {str(e)}")

    def key_takeaways(self, text: str) -> List[str]:
        if not text or len(text.strip()) == 0:
            raise Exception("No text provided for key takeaways.")
        prompt = (
            "List the 5 most important, precise, and meaningful key takeaways from the following text. "
            "Each takeaway should be a single line. Do not exceed 5 lines. Be clear and specific.\n\n"
            f"Text to analyze:\n{text[:8000]}\n\nKey takeaways (one per line):"
        )
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.5
            )
            takeaways_text = response.choices[0].message["content"].strip()
            lines = [line.lstrip('-•0123456789. ').strip() for line in takeaways_text.splitlines() if line.strip()]
            return lines[:5]
        except Exception as e:
            raise Exception(f"OpenAI error (key takeaways): {str(e)}")

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
        return [self.model]

    def test_connection(self) -> bool:
        try:
            prompt = "Hello!"
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            return True
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
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.5
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            raise Exception(f"OpenAI error (generate): {str(e)}") 