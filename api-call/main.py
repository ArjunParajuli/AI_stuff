from openai import OpenAI
from dotenv import load_dotenv
import os

# Loads .env file
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") 
)

response = client.chat.completions.create(
    model="meta-llama/llama-3.3-70b-instruct:free",  
    messages=[
        {
            "role": "user",
            "content": "Hey there, I am Arzun and nice to meet you."
        }
    ]
)

print(response.choices[0].message.content)
