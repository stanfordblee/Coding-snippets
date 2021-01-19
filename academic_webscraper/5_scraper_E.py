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
call_journal = "[Journal 5]"

# Parse in html request and make soup from DOM
html = requests.get("[Redacted]").text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# Find announcement notice box, which contains new calls
call_jmis_announce = soup.body.findAll("div", class_="alert alert-danger alert-dismissible")
# print(call_jmis_announce)

# Iterate through elements of announcement box
for call_jmis_element in call_jmis_announce:
    # If elements have links, text is call_title and href is call_details
    call_jmis_links = call_jmis_element.find("a")
    call_title = call_jmis_links.text
    # print(call_title)
    call_details = "https://www.jmis-web.org" + call_jmis_links.attrs['href']
    # print(call_details)

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