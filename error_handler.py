from functools import wraps
import logging
from typing import Callable, Any, Dict
from twilio.base.exceptions import TwilioRestException
from google.cloud.speech import SpeechClient
from google.api_core import exceptions as google_exceptions
import openai
from logger_config import get_logger

logger = get_logger(__name__)

class AIVoiceAgentError(Exception):
    """Base exception class for AI Voice Agent"""
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}

class SpeechProcessingError(AIVoiceAgentError):
    """Raised when speech processing fails"""
    pass

class AIProcessingError(AIVoiceAgentError):
    """Raised when AI processing fails"""
    pass

class CallHandlingError(AIVoiceAgentError):
    """Raised when call handling fails"""
    pass

def handle_twilio_errors(func: Callable) -> Callable:
    """Decorator to handle Twilio-related errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except TwilioRestException as e:
            error_msg = f"Twilio error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise CallHandlingError(
                message=error_msg,
                error_code="TWILIO_ERROR",
                details={"status": e.status, "code": e.code}
            )
    return wrapper

def handle_google_speech_errors(func: Callable) -> Callable:
    """Decorator to handle Google Speech-related errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except google_exceptions.GoogleAPIError as e:
            error_msg = f"Google Speech API error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise SpeechProcessingError(
                message=error_msg,
                error_code="GOOGLE_SPEECH_ERROR",
                details={"error_type": type(e).__name__}
            )
    return wrapper

def handle_openai_errors(func: Callable) -> Callable:
    """Decorator to handle OpenAI-related errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except openai.error.OpenAIError as e:
            error_msg = f"OpenAI API error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise AIProcessingError(
                message=error_msg,
                error_code="OPENAI_ERROR",
                details={"error_type": type(e).__name__}
            )
    return wrapper

def handle_general_errors(func: Callable) -> Callable:
    """Decorator to handle general errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise AIVoiceAgentError(
                message=error_msg,
                error_code="GENERAL_ERROR",
                details={"error_type": type(e).__name__}
            )
    return wrapper

def create_error_response(error: Exception) -> Dict[str, Any]:
    """Create a standardized error response"""
    if isinstance(error, AIVoiceAgentError):
        response = {
            "success": False,
            "error": {
                "message": str(error),
                "code": error.error_code,
                "details": error.details
            }
        }
    else:
        response = {
            "success": False,
            "error": {
                "message": str(error),
                "code": "UNKNOWN_ERROR",
                "details": {"error_type": type(error).__name__}
            }
        }
    return response

def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """Log error with context"""
    error_details = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {}
    }
    
    if isinstance(error, AIVoiceAgentError):
        error_details.update({
            "error_code": error.error_code,
            "details": error.details
        })
    
    logger.error(f"Error occurred: {error_details}", exc_info=True)
