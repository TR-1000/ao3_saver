# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:56:21 2019

@author: Miner
"""

import requests
from bs4 import BeautifulSoup
from datetime import date

url = "https://archiveofourown.org/works/23075947?view_full_work=true"

def save_to_file(url):
    req = requests.get(url)

    soup = BeautifulSoup(req.text, "html.parser")

    #Print title
    title_text = soup.title.text
    invalid_chars = ['<','>',':','"','/',"|",'?','/']
    title = title_text.strip()
    # remove invalid characters from title so it can be used as the file name
    for char in invalid_chars:
        if char in title:
            title = title.replace(char,'')
    complete_work = open(".\\sample_output\\"+title +".txt", "w", encoding='utf-8')
    complete_work.write(title + "\n\n")
    complete_work.write(f'URL: {url} \n')
    complete_work.write(f'Saved: {date.today()} \n')


    #Print stats
    stats_list = soup.find("dl", {"class": "stats"})
    stats = stats_list.find_all(["dt","dd"])
    for stat in stats:
        text = stat.text.strip()
        #Put dt and dd tag text on the same line instead of new line
        if ":" in text:
            complete_work.write(text + "  ")

        else:
            complete_work.write(text + "\n")



    #Remove stats row from metadata, since it has already been printed
    stats = soup.find_all(class_= "stats")
    for lines in stats:
        lines = lines.decompose()


    #Print meta data
    meta = soup.select('dl.work.meta.group')[0].find_all(['dt','dd'])
    for info in meta:
        text = info.text.strip()
        #Put dt and dd tag text on the same line instead of new line
        if ":" in text:
            complete_work.write(text + "  ")
        else:
            complete_work.write(text + "\n")


    #Print Summary
    summary = soup.find('div', {'class':'summary'})
    if summary:
        text = summary.p.text.strip()
        complete_work.write(f'\nSummary:\n{text}\n')


    #New Line splace
    new_line = ("\n")
    complete_work.write(new_line)


    #Main story text
    chapters = soup.find('div',{'id':'chapters'})
    tags = chapters.find_all(['h3','p','hr'])
    for lines in tags:
        #format spacing
        if "\n" in lines:
            #print(lines.text)
            complete_work.write(lines.text + "\n")
        else:
            lines = lines.text + "\n"
            complete_work.write(lines + "\n")



    complete_work.close()
    print('FINISHED!')

save_to_file(url)
