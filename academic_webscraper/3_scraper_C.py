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
call_journal = "[Journal 3]"

# Parse in html request and make soup from DOM
html = requests.get("[Redacted]").text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

call_jais_main = soup.body.findAll("div", id="main")
# print(call_jais_main)

# Find p class="journal follow" which to find preciding element of call information 
for call_jais_p in call_jais_main:
    call_jais_p_journal = call_jais_p.find("p", class_="journal-follow")
    # Iterate through next siblings to find next p tag, which contains call
    for iterator_p in call_jais_p_journal.next_siblings:
        if iterator_p.name == "p":
            call_jais_p_call = iterator_p

# Finding title by finding relevant call text section
call_jais_title_call = call_jais_p_call.findAll(text=re.compile("Special Issue Announcements"))

# For each call text, find text and href link of next sibling
for call_jais_text_call in call_jais_title_call:
    # print(call_jais_title_call)
    call_jais_item = call_jais_text_call.next_sibling


    # Find call_title and call_details
    call_title = call_jais_item.text[1:]
    # print(call_title)
    call_details = call_jais_item.attrs["href"]

    # Authors cannot be found on html page, only in pdf, so set as N/A
    call_authors = "N/A"

    # Due date cannot be found on html page, only in pdf, so set as Not Known
    call_due_date = "Not Known"

    # (For debugging) ensure that all entries are printed correctly
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