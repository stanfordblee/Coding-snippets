# Academic journal web scraper
# Created by Stanford Lee in December 2020

from bs4 import BeautifulSoup
import requests 
import pandas as pd
import re

# Make empty dataframe populated with headers
# This will be a template for the csv file later
df_call = pd.read_csv("data/export.csv", keep_default_na=False)
# print(df_call)

# Identify current journal 
call_journal = "[Journal 4]"

# Parse in html request and make soup from DOM
html = requests.get("[Redacted]").text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# Use id of the div containing call text to find subset of soup
call_jit_section = soup.body.find("div", id="rich-text-a5f7dc6a-6ee1-4cf1-b837-ded52de2db6d")
# print(call_jit_section)

# Find all href links, and find title and details from each href tag
call_jit_link = call_jit_section.findAll("a")
# print(call_jit_link)

for call_jit_elements in call_jit_link:
    # print(call_jit_elements)
    call_title = call_jit_elements.text
    # print(call_title)
    call_details = call_jit_elements.attrs["href"]
    # print(call_details)

    # Authors cannot be found on html page, only in pdf, so set as N/A
    call_authors = "N/A"

# # Find all associated dates
call_jit_dates = call_jit_section.findAll(text=re.compile("submissions:"))
# print(call_jit_dates)
for call_jit_date_elements in call_jit_dates:
    call_due_date = call_jit_date_elements.split(": ")[-1]
    

    # # (For debugging) ensure that all entries are printed correctly
    # print(call_title, call_details, call_authors, call_due_date)

    # Append call information as a new row of pandas dataframe, df_call
    df_call = df_call.append({"Journal": call_journal, 
                            "Title": call_title, 
                            "Authors": call_authors, 
                            "Due date": call_due_date, 
                            "Link": call_details
    }, ignore_index=True)

# print(df_call)

# # Export as CSV
df_call.to_csv("data/export.csv", index=False)
print("Updated 'export' CSV with call information from", call_journal)