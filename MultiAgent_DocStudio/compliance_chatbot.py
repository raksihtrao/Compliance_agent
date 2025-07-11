from llm_summarizer import LLMSummarizer

class ComplianceChatbot:
   
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = LLMSummarizer(model=model)

    def ask(self, question: str, context: str = None, chat_history: list = None) -> str:
    
        system_prompt = (
            "You are a compliance expert. Only answer questions related to compliance, regulations, and legal protocols. "
            "If a user asks about anything else, politely decline and redirect them to compliance topics. "
            "Always keep your answers focused on compliance issues."
        )
        history_str = ""
        if chat_history:
           
            for msg in chat_history[-4:]:
                role = msg.get('role', 'user')
                if role == 'user':
                    history_str += f"User: {msg['content']}\n"
                else:
                    history_str += f"Assistant: {msg['content']}\n"
        if context:
            prompt = (
                f"{system_prompt}\n\n"
                f"Context:\n{context}\n\n"
                f"{history_str}"
                f"User: {question}\nAssistant:"
            )
        else:
            prompt = (
                f"{system_prompt}\n\n"
                f"{history_str}"
                f"User: {question}\nAssistant:"
            )
        return self.llm.generate(prompt) 