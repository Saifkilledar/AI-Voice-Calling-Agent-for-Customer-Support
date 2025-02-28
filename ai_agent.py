import openai
import os
from typing import Dict, Any

class AIAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []
        
    def analyze_intent(self, user_input: str) -> Dict[str, Any]:
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Analyze intent using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a customer support AI analyzing user intent."},
                {"role": "user", "content": user_input}
            ]
        )
        
        # Extract intent from response
        intent_analysis = response.choices[0].message['content']
        
        # Simple intent categorization
        intent = {
            "category": self._categorize_intent(intent_analysis),
            "original_text": user_input,
            "confidence": 0.9  # Placeholder confidence score
        }
        
        return intent
    
    def generate_response(self, intent: Dict[str, Any]) -> str:
        # Generate appropriate response based on intent
        messages = [
            {"role": "system", "content": "You are a helpful customer support AI assistant. Provide clear and concise responses."},
            {"role": "user", "content": f"Generate a response for intent: {intent['category']}, user said: {intent['original_text']}"}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        ai_response = response.choices[0].message['content']
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        return ai_response
    
    def _categorize_intent(self, analysis: str) -> str:
        # Simple intent categorization logic
        lower_analysis = analysis.lower()
        
        if any(word in lower_analysis for word in ["help", "support", "assistance"]):
            return "general_help"
        elif any(word in lower_analysis for word in ["price", "cost", "payment"]):
            return "pricing"
        elif any(word in lower_analysis for word in ["technical", "error", "problem"]):
            return "technical_support"
        elif any(word in lower_analysis for word in ["account", "login", "password"]):
            return "account_support"
        else:
            return "general_inquiry"
    
    def reset_conversation(self):
        self.conversation_history = []
