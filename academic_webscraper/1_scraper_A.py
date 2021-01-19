# Academic journal web scraper
# Created by Stanford Lee in December 2020

from bs4 import BeautifulSoup
import requests 
import pandas as pd
import re

# Make empty dataframe populated with headers
# This will be a template for the csv file later
df_call = pd.DataFrame(columns=["Journal", 
                                "Title", 
                                "Authors", 
                                "Due date", 
                                "Link"
])
# print(df_call)

# Identify current journal 
call_journal = "[Journal 1]"

# Parse in html request and make soup from DOM
html = requests.get("[Redacted]").text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# Find call section, which is the only tbody section on the page
# This is right after static text header "Announcements"
call_isj_tbody = soup.body.findAll("tbody")
# print(call_isj_tbody)

# For each table row item in the table
# Iterating across table rows captures separate call entries
for call_isj_tr in call_isj_tbody:
    
    # find first td, which contains the title and link
    call_isj_td_title = call_isj_tr.findAll("td")[0]
    # find hyperlink tag, which contains title and link
    call_a_href = call_isj_td_title.findAll("a")
    # Save text from hyperlink tag as call_title (not title attribute)
    call_title = call_a_href[0].text

    # Save href attribute from hyperlink tag as call_details
    call_details = call_a_href[0].attrs["href"]

    # Authors cannot be found on html page, only in pdf, so set as N/A
    call_authors = "N/A"
    # print(call_authors)

    # find next td (2nd column of table), which contains the due date
    call_isj_td_due_date = call_isj_tr.findAll("td")[1]
    # Save tex tas call_due_date
    call_due_date = call_isj_td_due_date.text

    # (For debugging) ensure that all entries are printed correctly
    # print(call_title, call_details, call_authors, call_due_date, sep="\n")

    # Append call information as a new row of pandas dataframe, df_call
    df_call = df_call.append({"Journal": call_journal, 
                            "Title": call_title, 
                            "Authors": call_authors, 
                            "Due date": call_due_date, 
                            "Link": call_details
    }, ignore_index=True)
# print(df_call)

# Export as CSV
df_call.to_csv("data/export.csv", index=False)
print("Generated CSV titled 'export' in data folder")
print("Updated with call information from", call_journal)