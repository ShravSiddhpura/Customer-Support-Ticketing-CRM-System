import os
import requests
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
groq_client = Groq()

def get_ai_priority(description: str) -> str:
    """
    Attempts to get priority from completely free AI models.
    """
    prompt = f"""
    You are an expert technical support triage agent. 
    Read the following customer issue description and classify its priority as strictly one of: Low, Medium, or High.
    Do not output any introductory text, explanations, or punctuation. ONLY output the single word.
    
    Description: {description}
    """
    valid_priorities = ["Low", "Medium", "High"]
    
    # Strategy 1: Active Groq Model (Llama 3.1 8B)
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=10,
        )
        result = response.choices[0].message.content.strip()
        if result in valid_priorities:
            return result
    except Exception as e:
        print(f"Primary Groq model failed: {e}")

    # Strategy 2: Active Groq Fallback (Llama 3.3 70B)
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=10,
        )
        result = response.choices[0].message.content.strip()
        if result in valid_priorities:
            return result
    except Exception as e:
        print(f"Fallback Groq model failed: {e}")

    # Strategy 3: Active OpenRouter Fallback
    try:
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            }
            # Using the  Llama 3.1 endpoint
            payload = {
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 10
            }
            resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=5)
            resp.raise_for_status()
            
            result = resp.json()["choices"][0]["message"]["content"].strip()
            if result in valid_priorities:
                return result
    except Exception as e:
        print(f"OpenRouter fallback failed: {e}")

    # Ultimate Fallback: hardcoded default
    print("All AI providers failed. Defaulting to Medium.")
    return "Medium"