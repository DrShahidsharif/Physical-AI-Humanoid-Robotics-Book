import json
from datetime import datetime
from typing import List, Dict, Optional

# In-memory storage for chat history (as a fallback)
class ChatHistory:
    def __init__(self):
        self.history = []

    def add_entry(self, question: str, answer: str, context_used: Optional[str] = None):
        entry = {
            "id": len(self.history) + 1,
            "question": question,
            "answer": answer,
            "context_used": context_used,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.history.append(entry)
        return entry

    def get_all(self) -> List[Dict]:
        return self.history

    def get_latest(self, limit: int = 10) -> List[Dict]:
        return self.history[-limit:]

# Global instance
chat_history = ChatHistory()