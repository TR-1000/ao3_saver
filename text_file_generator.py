# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:56:21 2019

@author: Miner
"""

import requests
from bs4 import BeautifulSoup
from datetime import date

# url = "https://archiveofourown.org/works/23075947?view_full_work=true"

def save_to_file(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    #Get title of story
    title = soup.title.text.strip()
    invalid_chars = ['<','>',':','"','/',"|",'?','/']

    # remove invalid characters from title so it can be used as the file name
    for char in invalid_chars:
        if char in title:
            title = title.replace(char,'')

    with open(f'.\\output\\{title}.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(f'{title}\n\n')
        text_file.write(f'URL: {url} \n')
        text_file.write(f'Saved: {date.today()} \n')

        #Print stats
        stats_list = soup.find("dl", {"class": "stats"})
        stats = stats_list.find_all(["dt","dd"])
        for stat in stats:
            text = stat.text.strip()
            #Put dt and dd tag text on the same line instead of new line
            if ":" in text:
                text_file.write(text + "  ")

            else:
                text_file.write(text + "\n")


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
                text_file.write(text + "  ")
            else:
                text_file.write(text + "\n")


        #Print Summary
        summary = soup.find('div', {'class':'summary'})
        if summary:
            text = summary.p.text.strip()
            text_file.write(f'\nSummary:\n{text}\n')


        #New Line splace
        new_line = ("\n")
        text_file.write(new_line)


        #Main story text
        chapters = soup.find('div',{'id':'chapters'})
        tags = chapters.find_all(['h3','p','hr'])
        for lines in tags:
            #format spacing
            if "\n" in lines:
                #print(lines.text)
                text_file.write(lines.text + "\n")
            else:
                lines = lines.text + "\n"
                text_file.write(lines + "\n")


        print(f'{title} Saved!')

# save_to_file(url)
