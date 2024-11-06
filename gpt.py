from openai import OpenAI
import os

client = OpenAI()

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a number cruncher."},
            {"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.5
    )
    return response.choices[0].message.content

x = ["23, 45, 66, 44"]
print(chat_gpt(x[0] + "add these"))