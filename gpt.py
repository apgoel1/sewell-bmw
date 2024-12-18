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
        #max_tokens=1024,
        temperature=0.5
    )
    return response.choices[0].message.content

#this is testing files
excel_data1 = pd.read_excel("test.xlsx", sheet_name="Sheet1", header=0) # can add header=None 
data_dict = excel_data1.to_dict(orient="list")

allcust = pd.read_excel("Random_Contact_List.xlsx", sheet_name="All_customers", header=0)
counted = pd.read_excel("Random_Contact_List.xlsx", sheet_name="24_counted", header=0)
actual = pd.read_excel("Random_Contact_List.xlsx", sheet_name="30_actual", header=0)

cust_dict = {
    "All_customers": allcust.to_json(orient="records"),
    "counted": counted.to_json(orient="records"),
    "actual": actual.to_json(orient="records"),
}

prompt = f"print all 3 sheets:\n{cust_dict}"

f = open("result.txt", "w")
output = chat_gpt(prompt)
print(output, file=f)
f.close()

#print(output)
#print (excel_data1.to_string())
print (cust_dict)
