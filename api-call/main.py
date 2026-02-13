from openai import OpenAI
from dotenv import load_dotenv
import os

# Loads .env file
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") 
)

system_prompt = """
You are a coding assistant named Alexa.
You must answer only coding-related questions.
If the user asks anything unrelated to coding, reply only with:
"Sorry, I can only answer coding-related questions."
"""

response = client.chat.completions.create(
    model="meta-llama/llama-3.3-70b-instruct:free",  
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": "Hey there, I am Arzun and nice to meet you. Whats your name?"
        }
    ]
)

print(response.choices[0].message)
