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
call_journal = "[Journal 2]"

# Parse in html request and make soup from DOM
html = requests.get("[Redacted]").text
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

# Find only div items of slide item class, which contains the sidebar with call links
call_isr_div = soup.body.findAll("div", class_="slide-item")

# # Iterate through items in div
for call_isr_data in call_isr_div:
    # print(call_isr_data)

    # Find call_title when 'special issue' is mentioned
    call_isr_special = call_isr_data.findAll(text=re.compile("Special Issue"))
    for call_isr_title_item in call_isr_special:
        # Find parent, take text, and then split to extract clean title
        call_isr_title_raw = call_isr_title_item.parent
        call_title = call_isr_title_raw.text.split("ISR")[-1]
        # print(call_title)

    # Find call_details link in href tag where target = "_blank"
    call_isr_href = call_isr_data.findAll("a", target="_blank")
    for call_isr_href_item in call_isr_href:
        call_details = call_isr_href_item.attrs["href"]

        # Due date formatting is inconsistent between different calls, so set as Not Known
        call_due_date = "Not Known"

        # Go into 'more details' link for each html href to find author list
        html_authors = requests.get(call_details).text
        soup_authors = BeautifulSoup(html_authors, 'html.parser')
        # Find author name in metadata 
        call_authors_list = soup_authors.findAll("meta", attrs={"name": "dc.Contributor"})
        
        call_authors = []
        for call_author_name in call_authors_list:
            # Gets content from tags and use l strip method to remove double spaces
            call_authors_nl = re.sub(' +',' ',call_author_name.get("content"))
            # Convert newline separated elements into list
            call_authors.append(call_authors_nl)
        # Convert list into comma separated string
        call_authors = ", ".join(call_authors)
        # print(call_authors)


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