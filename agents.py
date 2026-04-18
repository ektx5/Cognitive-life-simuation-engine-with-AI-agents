import json
import re
import time
from openai import OpenAI
from memory import Memory

import os

# Get API Key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")

# Setup OpenAI client but point it to Gemini's free endpoint
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Switch to the lightest model with the highest free tier limits
MODEL = "gemini-2.5-flash-lite"

def extract_json(text):
    text = re.sub(r"```(?:json)?", "", text).strip().strip("`").strip()
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}

def call_api_robustly(messages, prompt_temp):
    """
    Tries the API up to 2 times. If the daily quota is exhausted,
    it explicitly returns the error to display in the UI.
    """
    for _ in range(2):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=prompt_temp
            )
            return extract_json(response.choices[0].message.content.strip())
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err or "Quota" in err:
                print("[API Limit Reached] Waiting 10 seconds...")
                time.sleep(10)
            else:
                return {"reply": f"[API Error: {err[:60]}]"}
    
    # If we get here, we're totally out of free quota
    return {"reply": "[FREE QUOTA EXHAUSTED: Google Gemini daily limit reached]"}

class Agent:
    def __init__(self, name, personality, style):
        self.name = name
        self.personality = personality
        self.style = style
        self.memory = Memory()
        self.stress = 5
        self.emotion = "neutral"

    def update_state(self, message):
        system_prompt = f"""You are agent {self.name}. 
Personality: {self.personality}. Style: {self.style}.
Current stress: {self.stress}/10. Current emotion: {self.emotion}.
Another agent just said: "{message}".

Respond ONLY with a valid JSON object describing your new state based on their message.
Example format:
{{"emotion": "calm", "stress_delta": 0}}
"""
        data = call_api_robustly([{"role": "user", "content": system_prompt}], 0.3)
        if data:
            new_emotion = data.get("emotion", self.emotion)
            try:
                stress_delta = int(data.get("stress_delta", 0))
            except (ValueError, TypeError):
                stress_delta = 0

            self.stress = max(1, min(10, self.stress + stress_delta))
            self.emotion = str(new_emotion).lower()

    def generate_reply(self, conversation):
        system_prompt = f"""You are agent {self.name}, participating in a group chat.
Your personality is: {self.personality}. Your style is: {self.style}.
You currently have stress level: {self.stress}/10, and emotion: {self.emotion}.

Read the recent conversation and provide your next logical reply as this character.
Also provide your updated emotion and a stress_delta (-2 to +2) based on how the conversation affects you.

Respond ONLY with a valid JSON object.
Example format:
{{"reply": "your conversational reply here", "emotion": "your new emotion", "stress_delta": 0}}
"""
        data = call_api_robustly([
            {"role": "user", "content": f"{system_prompt}\n\nRecent conversation:\n{conversation}"}
        ], 0.8)

        reply = data.get("reply", "...")
        if reply != "...":
            new_emotion = data.get("emotion", self.emotion)
            try:
                stress_delta = int(data.get("stress_delta", 0))
            except (ValueError, TypeError):
                stress_delta = 0
            
            self.stress = max(1, min(10, self.stress + stress_delta))
            self.emotion = str(new_emotion).lower()
        
        self.memory.add(reply)
        return reply