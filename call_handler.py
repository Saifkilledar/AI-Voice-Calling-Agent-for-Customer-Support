from twilio.rest import Client
import os
from typing import Dict, Any

class CallHandler:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)
        self.active_calls = {}
    
    def start_call(self, to_number: str, from_number: str) -> str:
        """
        Initiate a new call
        """
        call = self.client.calls.create(
            url='http://your-webhook-url/incoming_call',
            to=to_number,
            from_=from_number
        )
        
        self.active_calls[call.sid] = {
            'status': 'initiated',
            'to': to_number,
            'from': from_number,
            'duration': 0
        }
        
        return call.sid
    
    def end_call(self, call_sid: str):
        """
        End an active call
        """
        try:
            call = self.client.calls(call_sid).update(status='completed')
            if call_sid in self.active_calls:
                del self.active_calls[call_sid]
            return True
        except Exception as e:
            print(f"Error ending call: {e}")
            return False
    
    def get_call_status(self, call_sid: str) -> Dict[str, Any]:
        """
        Get the current status of a call
        """
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                'status': call.status,
                'duration': call.duration,
                'direction': call.direction,
                'answered_by': call.answered_by
            }
        except Exception as e:
            print(f"Error fetching call status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def transfer_call(self, call_sid: str, transfer_to: str):
        """
        Transfer an active call to another number
        """
        try:
            call = self.client.calls(call_sid).update(
                url=f'http://your-webhook-url/transfer/{transfer_to}',
                method='POST'
            )
            return True
        except Exception as e:
            print(f"Error transferring call: {e}")
            return False
    
    def record_call(self, call_sid: str):
        """
        Start recording a call
        """
        try:
            recording = self.client.calls(call_sid).recordings.create()
            return recording.sid
        except Exception as e:
            print(f"Error starting recording: {e}")
            return None
