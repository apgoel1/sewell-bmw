from openai import OpenAI
import os
import pandas as pd

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

excel_data1 = pd.read_excel("test.xlsx", sheet_name="Sheet1", header=None) # can add header=None 

prompt = f"list the overlapping values between the 2 columns:\n{excel_data1.to_string()}"

f = open("result.txt", "w")
output = chat_gpt(prompt)
print(output, file=f)
f.close()

#print(chat_gpt(prompt))
#print (excel_data1)