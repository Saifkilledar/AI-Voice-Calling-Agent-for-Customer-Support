from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
import os
from speech_processor import SpeechProcessor
from ai_agent import AIAgent
from call_handler import CallHandler

load_dotenv()

app = Flask(__name__)
speech_processor = SpeechProcessor()
ai_agent = AIAgent()
call_handler = CallHandler()

@app.route("/incoming_call", methods=['POST'])
def handle_incoming_call():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/process_speech', timeout=3)
    gather.say("Hello, I'm your AI customer support agent. How can I help you today?")
    response.append(gather)
    return str(response)

@app.route("/process_speech", methods=['POST'])
def process_speech():
    speech_result = request.values.get('SpeechResult')
    if not speech_result:
        return handle_no_input()
    
    # Process speech and get AI response
    intent = ai_agent.analyze_intent(speech_result)
    response = ai_agent.generate_response(intent)
    
    # Generate TwiML response
    twiml = VoiceResponse()
    twiml.say(response)
    
    # Continue listening
    gather = Gather(input='speech', action='/process_speech', timeout=3)
    gather.say("Is there anything else I can help you with?")
    twiml.append(gather)
    
    return str(twiml)

@app.route("/hangup", methods=['POST'])
def handle_hangup():
    response = VoiceResponse()
    response.say("Thank you for calling. Goodbye!")
    response.hangup()
    return str(response)

def handle_no_input():
    response = VoiceResponse()
    response.say("I didn't catch that. Could you please repeat?")
    gather = Gather(input='speech', action='/process_speech', timeout=3)
    response.append(gather)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
