from openai import OpenAI
import os

client = OpenAI()

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a number cruncher."},
            {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

x = input("How can ai help you today?")
print(chat_gpt(x))