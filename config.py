import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
FLASK_DEBUG = True
FLASK_PORT = 5000
FLASK_HOST = '0.0.0.0'

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Call Settings
MAX_CALL_DURATION = 30 * 60  # 30 minutes
SPEECH_TIMEOUT = 3  # seconds
MAX_RETRIES = 3

# AI Agent Settings
AI_CONFIDENCE_THRESHOLD = 0.7
DEFAULT_LANGUAGE = 'en-US'

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
