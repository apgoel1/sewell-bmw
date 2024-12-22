from openai import OpenAI
import os
import pandas as pd
import spacy

client = OpenAI()

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "data analyzer"},
            {"role": "user", "content": prompt}],
        #max_tokens=1024,
        temperature=0.5
    )
    return response.choices[0].message.content

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 3000)


#this is testing files
excel_data1 = pd.read_excel("test.xlsx", sheet_name="Sheet1", header=0) # can add header=None 
data_dict = excel_data1.to_dict(orient="list")

#converting all the sheets into pandas for analysis
allcust = pd.read_excel("Random_Contact_List.xlsx", sheet_name="All_customers", header=0)
counted = pd.read_excel("Random_Contact_List.xlsx", sheet_name="24_counted", header=0)
actual = pd.read_excel("Random_Contact_List.xlsx", sheet_name="30_actual", header=0)

nlp = spacy.load("en_core_web_md")
doc1 = nlp("a")
doc2 = nlp("z")

print(doc1.similarity(doc2))

cust_dict = {
    "All_customers": allcust.to_json(orient="records"),
    "counted": counted.to_json(orient="records"),
    "actual": actual.to_json(orient="records"),
}

prompt = f"how many people have the same name: \n{allcust}"

f = open("result.txt", "w")
#output = chat_gpt(prompt)
#print(output, file=f)
#print(allcust, file=f)
f.close()

#print(output)
#print (excel_data1.to_string())
#print (allcust)
