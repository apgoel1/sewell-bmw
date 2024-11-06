import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or use 'gpt-4-turbo' for the more efficient variant
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150  # Adjust the response length as needed
    )
    return response['choices'][0]['message']['content']

prompt = "Explain the basics of accounting."
output = generate_text(prompt)
print(output)