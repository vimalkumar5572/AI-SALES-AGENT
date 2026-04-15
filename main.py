from fastapi import FastAPI, Form, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from dotenv import load_dotenv
from openai import OpenAI
import os
import uvicorn

load_dotenv()

app = FastAPI(title="AI Sales Agent")

twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"), 
    os.getenv("TWILIO_AUTH_TOKEN")
)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

PUBLIC_BASE_URL = "https://amuser-ending-antirust.ngrok-free.dev"

@app.get("/")
def home():
    return {"message": "✅ AI Sales Agent chal raha hai! 🔥"}

@app.post("/make-call")
def make_outbound_call(to_phone: str):
    print(f"📞 Call initiating to: {to_phone}")
    call = twilio_client.calls.create(
        to=to_phone,
        from_=TWILIO_NUMBER,
        url=f"{PUBLIC_BASE_URL}/voice",
        method="POST"
    )
    print(f"✅ Call initiated | SID: {call.sid}")
    return {"status": "Call initiated", "call_sid": call.sid}

# ================== VOICE WEBHOOK ==================
@app.post("/voice")
async def voice_webhook():
    print("🎤 /voice webhook HIT hua hai! Twilio ne request bheji")
    
    resp = VoiceResponse()
    resp.say("Namaste! Main AI Sales Agent hoon. Aapka naam kya hai?", 
             voice="Polly.Aditi")
    
    gather = Gather(input="speech", action="/gather", language="hi-IN", timeout=8)
    resp.append(gather)
    
    print("✅ TwiML response Twilio ko bheja gaya")
    return Response(content=str(resp), media_type="text/xml")

# ================== AI CONVERSATION ==================
@app.post("/gather")
async def gather_speech(SpeechResult: str = Form(...)):
    user_input = SpeechResult.strip()
    print(f"👤 User bola: {user_input}")
    
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a friendly Hindi-English sales agent."},
            {"role": "user", "content": user_input}
        ]
    )
    ai_reply = completion.choices[0].message.content
    print(f"🤖 AI jawab: {ai_reply}")

    resp = VoiceResponse()
    resp.say(ai_reply, voice="Polly.Aditi")
    
    gather = Gather(input="speech", action="/gather", language="hi-IN", timeout=8)
    resp.append(gather)
    
    return Response(content=str(resp), media_type="text/xml")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)