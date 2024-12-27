import streamlit as st
import pandas as pd
import os
from openai import OpenAI
import time

starttime = time.time()
# Initialize OpenAI client
client = OpenAI()

# ChatGPT interaction functions
def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Always respond with data formatted as a table"},
            {"role": "user", "content": prompt}],
        temperature=0.6
    )
    return response.choices[0].message.content

def chat_gpt_compare(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Always respond with one word"},
            {"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

def file_comparer(fa, fb, comp_prompt):
    with open(fa, "r") as filea, open(fb, "r") as fileb:
        content1 = filea.read()
        content2 = fileb.read()
    prompt = f"{comp_prompt} \n{content1} \n{content2}"
    return chat_gpt_compare(prompt)

def pick_longer(fa, fb, res):
    with open(fa, "r") as filea, open(fb, "r") as fileb:
        content1 = filea.read()
        content2 = fileb.read()
        filea.seek(0)
        fileb.seek(0)
        linecounta = len(filea.readlines())
        linecountb = len(fileb.readlines())

    with open(res, "w") as r:
        if linecounta > linecountb:
            print(content1, file=r)
        else:
            print(content2, file=r)

# Streamlit App
st.title("Customer Analysis Tool")
st.write("Upload an Excel file to analyze customer data.")
# want to add a section here about entering user's own names for the sheets in the file
# maybe even allow the user to enter their own prompt (or select from a few exisiting options (drop down menu))


# File Upload Section
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    st.success("File uploaded successfully!")

    #displays the full pandas dataframe rather than truncating
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 3000)

    # Read Excel file into Pandas dataframes
    allcust = pd.read_excel(uploaded_file, sheet_name="All_customers", header=0)
    counted = pd.read_excel(uploaded_file, sheet_name="24_counted", header=0)
    actual = pd.read_excel(uploaded_file, sheet_name="30_actual", header=0)

    # Dictionary for analysis
    cust_dict = {
        "All_customers": allcust,
        "counted": counted,
        "actual": actual,
    }

    main_prompt = f"identify the people who are in actual that weren't counted that are also part of allcust. only 2 fields must match: \n{cust_dict}"
    main_promptg = f"how many unique names in allcust?: \n{cust_dict}"


    # Process with OpenAI GPT
    if st.button("Analyze"):
        with st.spinner("Processing..."):
            f = open("A.txt", "w")
            outputA = chat_gpt(main_prompt)
            print(outputA, file=f)
            f.close()

            g = open("B.txt", "w")
            outputB = chat_gpt(main_prompt)
            print(outputB, file=g)
            g.close()

            compare_prompt = "Is the information presented in these two files essentially the same?"
            yn = file_comparer("A.txt", "B.txt", compare_prompt)

            counter = 0
            while (yn[0] != "Y") and (counter < 3):
                pick_longer("A.txt", "B.txt", "A.txt")
                g = open("B.txt", "w")
                outputB = chat_gpt(main_prompt)
                print(outputB, file=g)
                g.close()
                yn = file_comparer("A.txt", "B.txt", compare_prompt)
                counter += 1

            pick_longer("A.txt", "B.txt", "result.txt")

            with open("result.txt", "r") as result_file:
                result_content = result_file.read()

        st.success("Analysis complete!")
        st.write("### Result")
        st.text(result_content)

         # Show elapsed runtime
        endtime = time.time()
        st.write(f"Elapsed time: {endtime - starttime} seconds")
        if (counter == 3):
            st.warning('''
                       Consider running program again for better result  
                       If this occurs again, GPT could be having difficulty working with the data and may not be perfect
                       ''')
        st.download_button("Download Result", result_content, "final_result.txt")
    else:
        st.write("Press 'Analyze' button to start")