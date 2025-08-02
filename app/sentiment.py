import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def analyze_sentiment(text: str) -> str:
    prompt = f"""
You are a financial sentiment classifier. 
Given the headline below, classify the sentiment as exactly one of: 'positive', 'negative', or 'neutral'. 
Headline: "{text}"
Only reply with one word: positive, negative, or neutral.
"""


    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Adjust if you're using a different version
        messages=[
            {"role": "system", "content": "You are a financial sentiment classifier."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=10,
    )

    result = response.choices[0].message.content.strip().lower()

    # Validate result to prevent junk responses
    if result in ["positive", "negative", "neutral"]:
        return result
    else:
        return "neutral"  # Fallback default
