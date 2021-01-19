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
call_journal = "[Journal 6]"

# Parse in html request and make soup from DOM
html = requests.get("[Redacted]").text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# Directly find calls by searching for 'announcements' string
call_misq_string_list = soup.body.findAll(text=re.compile("Announcements"))
for call_misq_string in call_misq_string_list:
    
    # Find title by splitting strings after "Announcements" substrings
    call_title = call_misq_string.split(": ")[-1].strip()
    call_misq_link = call_misq_string.parent
    # Find link based on href
    call_details = call_misq_link.attrs["href"]

    # callauthors are siblings of the link, 4 spaces away
    call_author_raw = call_misq_link.next_sibling.next_sibling.next_sibling

    # Strip whitespace and "by " string 
    call_author_fix = call_author_raw.strip()
    call_author_spl = call_author_fix.split("by ")
    # If there were no authors, return N/A
    if len(call_author_spl) > 1:
        call_authors = call_author_spl[-1]
    else:
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