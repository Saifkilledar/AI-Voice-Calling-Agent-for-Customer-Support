import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib
import os
from config import LOG_LEVEL, LOG_FORMAT

# Set up logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class CallUtils:
    @staticmethod
    def generate_call_id(phone_number: str) -> str:
        """Generate a unique call ID based on phone number and timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_string = f"{phone_number}{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        """Basic phone number validation"""
        # Remove any non-numeric characters
        cleaned = ''.join(filter(str.isdigit, phone_number))
        # Check if the number has a valid length
        return 10 <= len(cleaned) <= 15

    @staticmethod
    def format_phone_number(phone_number: str) -> str:
        """Format phone number to E.164 format"""
        cleaned = ''.join(filter(str.isdigit, phone_number))
        if not cleaned.startswith('1'):
            cleaned = '1' + cleaned
        return f"+{cleaned}"

class ConversationUtils:
    @staticmethod
    def save_conversation(call_id: str, conversation: list) -> bool:
        """Save conversation history to a file"""
        try:
            filename = f"conversations/{call_id}.json"
            os.makedirs("conversations", exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(conversation, f)
            return True
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            return False

    @staticmethod
    def load_conversation(call_id: str) -> Optional[list]:
        """Load conversation history from a file"""
        try:
            filename = f"conversations/{call_id}.json"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading conversation: {e}")
        return None

class AudioUtils:
    @staticmethod
    def convert_audio_format(audio_data: bytes, source_format: str, target_format: str) -> Optional[bytes]:
        """Convert audio between different formats"""
        try:
            # Implementation would depend on audio processing library
            # This is a placeholder for the actual implementation
            return audio_data
        except Exception as e:
            logger.error(f"Error converting audio format: {e}")
            return None

    @staticmethod
    def detect_silence(audio_data: bytes, threshold: float = 0.1) -> bool:
        """Detect if audio contains silence"""
        try:
            # Implementation would depend on audio processing library
            # This is a placeholder for the actual implementation
            return False
        except Exception as e:
            logger.error(f"Error detecting silence: {e}")
            return True

class MetricsUtils:
    @staticmethod
    def log_metric(metric_name: str, value: Any, tags: Dict[str, str] = None):
        """Log a metric for monitoring"""
        try:
            timestamp = datetime.now().isoformat()
            metric = {
                'name': metric_name,
                'value': value,
                'timestamp': timestamp,
                'tags': tags or {}
            }
            logger.info(f"Metric: {json.dumps(metric)}")
        except Exception as e:
            logger.error(f"Error logging metric: {e}")

class SecurityUtils:
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        # Remove any potentially dangerous characters or patterns
        return text.replace('<', '').replace('>', '').replace('"', '').replace("'", '')

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format"""
        # Basic validation - should be replaced with proper validation logic
        return bool(api_key and len(api_key) >= 32)

    @staticmethod
    def mask_sensitive_data(text: str) -> str:
        """Mask sensitive data in logs"""
        # Add patterns for sensitive data (credit cards, SSNs, etc.)
        patterns = {
            r'\b\d{16}\b': '****-****-****-****',  # Credit card
            r'\b\d{3}-\d{2}-\d{4}\b': '***-**-****',  # SSN
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': '****@****.***'  # Email
        }
        masked = text
        for pattern, mask in patterns.items():
            masked = masked.replace(pattern, mask)
        return masked
