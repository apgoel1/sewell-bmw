from openai import OpenAI
import os
import pandas as pd
#import spacy # used for nlp and similarity score (semantic/meaning based)
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

# making a separate function for this is ok because it helps ensure consistency and role/temperature values
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

def file_comparer(fa, fb, comp_prompt):
    # comparing the first and second iterations
    with open(fa, "r") as filea, open(fb, "r") as fileb:
        content1 = filea.read()
        content2 = fileb.read()
    # if they are the same, it is more likely that gpt did not make a mistake (but still very possible)
    prompt = f"{comp_prompt} \n{content1} \n{content2}"
    # compare the two results from running the gpt twice
    answer = chat_gpt_compare(prompt) # gives a Yes or No

    return answer

# added this function to condense code
def pick_longer(fa, fb, res):
     # in my use case, more rows likely means a better result, so I want to store that result
    with open(fa, "r") as filea, open(fb, "r") as fileb:
        content1 = filea.read() # puts the content into a string
        content2 = fileb.read()
        filea.seek(0)  # Reset the file pointer to the start
        fileb.seek(0)  
        linecounta = len(filea.readlines()) # counts the number of lines in each file
        linecountb = len(fileb.readlines())

    if (linecounta > linecountb): #overwrites the "better" file to a result file
        r = open(res, "w")
        print(content1, file=r)
        r.close()
    else:
        r = open(res, "w")
        print(content2, file=r)
        r.close()

#displays the full pandas dataframe rather than truncating
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 3000)

#converting all the sheets into pandas for analysis
allcust = pd.read_excel("Random_Contact_List.xlsx", sheet_name="All_customers", header=0)
counted = pd.read_excel("Random_Contact_List.xlsx", sheet_name="24_counted", header=0)
actual = pd.read_excel("Random_Contact_List.xlsx", sheet_name="30_actual", header=0)

# can use this to print specific values from data frame
#print (allcust["Name"][10])

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

# if they are the same, it is more likely that gpt did not make a mistake (but still very possible)
compare_prompt = f"Is the information presented in these two files essentially the same?"
# comparing the first and second iterations
yn = file_comparer("A.txt", "B.txt", compare_prompt)

counter = 0 # initalizing counter for upcoming while loop

#loop for trying to get consistent results (sometimes gpt can make mistakes) (3 seems like a reasonable number of times to try)
while((yn[0] != "Y") and (counter < 3)):

    # in my use case, more rows likely means a better result, so I want to store that result
    pick_longer("A.txt", "B.txt", "A.txt")

    #generate another output and compare the original "good" one
    g = open("B.txt", "w")
    outputB = chat_gpt(main_prompt)
    print(outputB, file=g)
    g.close()

    #continues to compare the two files until they are the same or the counter reaches a certain number
    yn = file_comparer("A.txt", "B.txt", compare_prompt)
    counter += 1


pick_longer("A.txt", "B.txt", "result.txt")

print(counter)

endtime = time.time()
print(f"Elapsed time: {endtime-starttime} seconds")