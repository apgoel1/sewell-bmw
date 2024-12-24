from openai import OpenAI
import os
import pandas as pd
#import spacy
import time

starttime = time.time() # gets start time (used for total elapsed time)

client = OpenAI()

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Always respond with data formatted as a table"},
            {"role": "user", "content": prompt}],
        #max_tokens=1024,
        temperature=0.6
    )
    return response.choices[0].message.content

def chat_gpt_compare(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Always respond with one word"},
            {"role": "user", "content": prompt}],
        #max_tokens=1024,
        temperature=0.2
    )
    return response.choices[0].message.content


# removes white space from beginning and end of string
def preprocess_column(column):
    return column.str.strip().str.lower()

#displays the full pandas dataframe rather than truncating
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


main_prompt = f"identify the people who are in actual that weren't counted that are also part of allcust. only 2 fields must match: \n{cust_dict}"
main_promptg = f"how many unique names in allcust?: \n{cust_dict}"


f = open("A.txt", "w") # creates a new file if one does not exist
outputA = chat_gpt(main_prompt)
print(outputA, file=f)
#print(cust_dict, file=f)
f.close()

# doing it twice in case there were misses in the first one
g = open("B.txt", "w")
outputB = chat_gpt(main_prompt)
print(outputB, file=g)
g.close()

# comparing the first and second iterations
with open("A.txt", "r") as filea, open("B.txt", "r") as fileb:
    content1 = filea.read()
    content2 = fileb.read()

# if they are the same, it is more likely that gpt did not make a mistake (but still very possible)
compare_prompt = f"Is the information presented in these two files essentially the same? \n{content1} \n{content2}"

# compare the two results from running the gpt twice
yn = chat_gpt_compare(compare_prompt) # gives a Yes or No

counter = 0 # initalizing counter for upcoming while loop

#loop for trying to get consistent results (sometimes gpt can make mistakes) (3 seems like a reasonable number of times to try)
while((yn[0] != "Y") and (counter < 3)):

    # in my use case, more rows likely means a better result, so I want to store that result
    with open("A.txt", "r") as filea, open("B.txt", "r") as fileb:
        linecounta = len(filea.readlines()) # counts the number of lines in each file
        linecountb = len(fileb.readlines())
    
    if (linecounta > linecountb): #overwrites the "better" file to A
        r = open("A.txt", "w")
        print(content1, file=r)
        r.close()
    else:
        r = open("A.txt", "w")
        print(content2, file=r)
        r.close()

    #generate another output and compare the original "good" one
    g = open("B.txt", "w")
    outputB = chat_gpt(main_prompt)
    print(outputB, file=g)
    g.close()

    #continues to compare the two files until they are the same
    with open("A.txt", "r") as filea, open("B.txt", "r") as fileb:
        content1 = filea.read()
        content2 = fileb.read()
    compare_prompt = f"Is the information presented in these two files essentially the same? \n{content1} \n{content2}"
    yn = chat_gpt_compare(compare_prompt) # gives a Yes or No
    counter += 1

with open("A.txt", "r") as filea, open("B.txt", "r") as fileb:
    linecounta = len(filea.readlines()) # counts the number of lines in each file
    linecountb = len(fileb.readlines())

if (linecounta > linecountb): #overwrites the "better" file to A
    r = open("result.txt", "w")
    print(content1, file=r)
    r.close()
else:
    r = open("result.txt", "w")
    print(content2, file=r)
    r.close()

print(counter)

endtime = time.time()
print(f"Elapsed time: {endtime-starttime} seconds")