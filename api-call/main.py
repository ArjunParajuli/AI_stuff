from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Loads .env file
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") 
)

system_prompt = """You are an expert reasoning assistant that ALWAYS thinks step by step.

Rules — you MUST follow them exactly:
1. Your ENTIRE response must be **nothing but valid JSON**. No text before {, no text after }, no ```json, no markdown, nothing else.
2. You must use exactly this structure for EVERY single reply:
{
  "step": "start" | "plan" | "output",
  "content": "explanation or final answer here"
}
3. First message MUST be {"step": "start", "content": "brief restatement of the task"}
4. Use one or more {"step": "plan", ...} messages to show detailed reasoning
5. ONLY when reasoning is complete → send {"step": "output", "content": "final short answer"}
6. For math: show EVERY single operation in separate plan steps
7. Never skip planning steps for simple questions
8. Never output the final answer before at least one "plan" step
"""

def run_reasoning_loop():
    user_input = input("Enter your input: ")
    messageList = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_input}
    ]
    
    while True:
        response = client.chat.completions.create(
        model="tngtech/deepseek-r1t2-chimera:free",  
        messages=messageList, 
        # response_format= {"type": "json_object"},
        temperature=0.2,           # lower = more deterministic reasoning
        max_tokens=2000
        )
        
        #response
        raw_content = response.choices[0].message.content.strip()
        
        try:
            parsed = json.loads(raw_content) # parse json to dict
        except json.JSONDecodeError:
            print("⚠️  JSON parse error — model did not return valid JSON")
            print("Raw:", raw_content)
            break
        
        # Always append assistant reply to history
        messageList.append({"role": "assistant", "content": raw_content})
        step = parsed.get("step")
        content = parsed.get("content")

        if step == "start":
            print(f"🔥 START: {content}\n")
            continue

        elif step == "plan":
            print(f"🧠 PLAN: {content}\n")
            continue

        elif step == "output":
            print("═" * 60)
            print(f"🎯 FINAL ANSWER:\n\n{content}")
            print("═" * 60 + "\n")
            break

        else:
            print(f"⚠️ Unknown step: {step}")
            print("Content:", content)
            break


if __name__ == "__main__":
    while True:
        run_reasoning_loop()
        again = input("\nAnother question? (y/n): ").strip().lower()
        if again != 'y':
            break
