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
Convert Sentiment to the mood of the user
"""

user_input = "I hate it"

response = client.chat.completions.create(
        model="stepfun/step-3.5-flash:free",  
    messages=[
        {"role": "system", "content": system_prompt},
    
        # Example 1
        {"role": "user", "content": "Love this product!"},
        {"role": "assistant", "content": "Happy"},
        
        # Actual user input
        {"role": "user", "content": user_input}
        ]
)

print(response.choices[0].message)
