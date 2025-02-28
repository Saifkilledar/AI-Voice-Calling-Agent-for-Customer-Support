import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speech_processor import SpeechProcessor
from ai_agent import AIAgent
from call_handler import CallHandler
from utils import CallUtils, ConversationUtils, SecurityUtils

class TestSpeechProcessor(unittest.TestCase):
    def setUp(self):
        self.speech_processor = SpeechProcessor()

    def test_speech_to_text(self):
        # Mock audio content for testing
        audio_content = b"mock_audio_content"
        result = self.speech_processor.speech_to_text(audio_content)
        self.assertIsInstance(result, str)

    def test_text_to_speech(self):
        text = "Hello, this is a test"
        result = self.speech_processor.text_to_speech(text)
        self.assertIsInstance(result, bytes)

class TestAIAgent(unittest.TestCase):
    def setUp(self):
        self.ai_agent = AIAgent()

    def test_analyze_intent(self):
        user_input = "I need help with my account"
        intent = self.ai_agent.analyze_intent(user_input)
        self.assertIsInstance(intent, dict)
        self.assertIn('category', intent)
        self.assertIn('original_text', intent)
        self.assertIn('confidence', intent)

    def test_generate_response(self):
        intent = {
            'category': 'account_support',
            'original_text': 'I need help with my account',
            'confidence': 0.9
        }
        response = self.ai_agent.generate_response(intent)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

class TestCallHandler(unittest.TestCase):
    def setUp(self):
        self.call_handler = CallHandler()

    def test_get_call_status(self):
        call_sid = "test_call_sid"
        status = self.call_handler.get_call_status(call_sid)
        self.assertIsInstance(status, dict)
        self.assertIn('status', status)

class TestUtils(unittest.TestCase):
    def test_call_utils(self):
        phone_number = "1234567890"
        call_id = CallUtils.generate_call_id(phone_number)
        self.assertIsInstance(call_id, str)
        self.assertEqual(len(call_id), 32)  # MD5 hash length

        is_valid = CallUtils.validate_phone_number(phone_number)
        self.assertTrue(is_valid)

        formatted = CallUtils.format_phone_number(phone_number)
        self.assertTrue(formatted.startswith('+'))

    def test_conversation_utils(self):
        call_id = "test_call_id"
        conversation = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        success = ConversationUtils.save_conversation(call_id, conversation)
        self.assertTrue(success)

        loaded = ConversationUtils.load_conversation(call_id)
        self.assertEqual(loaded, conversation)

    def test_security_utils(self):
        input_text = "<script>alert('test')</script>"
        sanitized = SecurityUtils.sanitize_input(input_text)
        self.assertNotIn('<script>', sanitized)

        api_key = "a" * 32
        is_valid = SecurityUtils.validate_api_key(api_key)
        self.assertTrue(is_valid)

        sensitive_text = "My credit card is 1234-5678-9012-3456"
        masked = SecurityUtils.mask_sensitive_data(sensitive_text)
        self.assertNotIn("1234-5678-9012-3456", masked)

if __name__ == '__main__':
    unittest.main()
