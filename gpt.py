from openai import OpenAI
import os
import pandas as pd
#import spacy

client = OpenAI()

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Always respond with data formatted as a table"},
            {"role": "user", "content": prompt}],
        #max_tokens=1024,
        temperature=0.2
    )
    return response.choices[0].message.content

# removes white space from beginning and end of string
def preprocess_column(column):
    return column.str.strip().str.lower()

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

# can use this to print specific values from data frame
#print (allcust["Name"][10])

# ai used for similarity (semantic/meaning based)
#nlp = spacy.load("en_core_web_md")
#doc1 = nlp("a")
#doc2 = nlp("z")
#print(doc1.similarity(doc2))

#dictionary makes it easier for gpt to analyze
cust_dict = {
    "All_customers": allcust,
    "counted": counted,
    "actual": actual,
}

prompt = f"identify the people who are in actual that weren't counted that are also part of allcust. only 2 fields must match: \n{cust_dict}"
#prompt = f"did alex rodriguez move houses?: \n{cust_dict}"

#f = open("result.txt", "w")
#output = chat_gpt(prompt)
#print(output, file=f)
#print(cust_dict, file=f)
#f.close()

#g = open("result2.txt", "w")
#output2 = chat_gpt(prompt)
#print(output2, file=g)
#g.close()

with open("result.txt", "r") as file1, open("result2.txt", "r") as file2:
    content1 = file1.read()
    content2 = file2.read()

prompt2 = f"Is the information presented in these two files essentially the same? \n{content1} \n{content2}"


output2 = chat_gpt(prompt2)
print(output2)

#print(output)
#print (excel_data1.to_string())
#print (cust_dict)
