import json
import os
import requests
from src.utils.vector_store import retrieve_similar
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

import asyncio

async def get_explanation(signal_path):
    with open(signal_path, 'r') as f:
        signal = json.load(f)
    query = signal['meta']['reason']
    docs = await retrieve_similar(query)
    prompt = f"Explain the trading signal: {json.dumps(signal)}\nRelevant docs: {docs}"
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY must be set in .env or environment variables.")
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload))
    if response.status_code == 200:
        result = response.json()
        explanation = result['candidates'][0]['content']['parts'][0]['text']
        return explanation
    else:
        return f"Trade reason: {query}\nRelevant docs: {docs}\nLLM error: {response.text}"
