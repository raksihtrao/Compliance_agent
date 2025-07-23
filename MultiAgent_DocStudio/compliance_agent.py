import json
from typing import List, Dict, Optional
from llm_summarizer import LLMSummarizer
from storage_manager import StorageManager
import re

class ComplianceAgent:
   
    def __init__(self, domain: str = "GDPR", rules: Optional[List[Dict]] = None, provider: str = "openai", model: str = "gpt-3.5-turbo"):
        self.domain = domain
        self.rules = rules or []
        self.llm = LLMSummarizer(provider=provider, model=model)
        self.storage = StorageManager()

    def ingest_and_chunk(self, text: str, chunk_size: int = 1200) -> List[str]:
        
        
        paragraphs = text.split('\n\n')
        chunks = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) < chunk_size:
                current += para + "\n\n"
            else:
                if current:
                    chunks.append(current.strip())
                current = para + "\n\n"
        if current:
            chunks.append(current.strip())
        return chunks

    def build_prompt(self, chunk: str) -> str:
        
        return (
            f"You are a compliance analyst. Review the following text and analyze it strictly according to the provided compliance protocol. "
            f"Output a JSON object with the following fields: compliance_summary (a short summary of how compliant the document is), "
            f"approvals (list of compliant points), violations (list of non-compliant points). Cite specific clauses if possible.\n"
            f"\nExample JSON output:\n"
            f"{{\n  \"compliance_summary\": \"<summary>\",\n  \"approvals\": [\"<point1>\", \"<point2>\"],\n  \"violations\": [\"<violation1>\", \"<violation2>\"]\n}}\n"
            f"\nText to check:\n{chunk}"
        )

    def _extract_json(self, text: str) -> str:
       
        
        text = text.strip()
        text = re.sub(r'^```[a-zA-Z]*', '', text)
        text = re.sub(r'```$', '', text)
       
        match = re.search(r'\{[\s\S]*?\}', text)
        if match:
            return match.group(0)
        return text  

    def check_compliance(self, text: str, custom_prompt: str = None) -> List[Dict]:
       
        chunks = self.ingest_and_chunk(text)
        results = []
        
        for chunk in chunks:
            if custom_prompt:
                prompt = f"{custom_prompt}\n\nPlease output ONLY valid JSON in the following format (no explanation):\n{{\n  \"compliance_summary\": \"<summary>\",\n  \"approvals\": [\"<point1>\", \"<point2>\"],\n  \"violations\": [\"<violation1>\", \"<violation2>\"]\n}}\n\nDocument to analyze:\n{chunk}"
            else:
                prompt = self.build_prompt(chunk)
            
            llm_response = self.llm.generate(prompt)
            
            json_str = self._extract_json(llm_response)
            try:
                parsed = json.loads(json_str)
            except Exception as e:
                parsed = {
                    "compliance_summary": "Parsing Error: The LLM did not return valid JSON. Treating as non-compliant.",
                    "approvals": [],
                    "violations": [
                        f"LLM output could not be parsed as JSON. Raw output: {llm_response[:200]}...",
                        f"Parsing error: {str(e)}"
                    ],
                    "raw_output": llm_response,
                    "parsing_error": str(e)
                }
            if self.rules:
                parsed = self.cross_reference_rules(parsed, chunk)
            results.append(parsed)
        return results

    def cross_reference_rules(self, llm_output: Dict, chunk: str) -> Dict:
        #Cross-referencing LLM output
        
        llm_output['rules_checked'] = [rule.get('name') for rule in self.rules]
        return llm_output

    def save_report(self, report: List[Dict], filename: str = "compliance_report.json"):
        #Saving the compliance report using the storage manager.
        self.storage.save_to_json({"domain": self.domain, "results": report, "filename": filename}) 