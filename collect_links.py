import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)
from bs4 import BeautifulSoup
from datetime import date
from text_file_generator import save_to_file



# This script collects all links for a 'fandom', in this case the Star Wars Prequel Trilogy fandom. Because I love the Prequel Trilogy.

fandom = {
    'name': 'Star Wars Prequel Trilogy',
    'url': "https://archiveofourown.org/tags/Star%20Wars%20Prequel%20Trilogy/works?page=12&view_adult=true",
    'stories': []
}

url = fandom['url']
while url:
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        works = soup.select('div.header.module')

        for work in works:
            try:
                fandom_tags = work.select('h5 a')
                try:
                    author_name = work.find('a',{'rel':'author'}).text
                    # If the author is anonymous or has no link this won't work
                except:
                    # This code finds the author name if it's not in an <a> tag
                    by_line = work.h4.text.strip()
                    author_name = by_line[by_line.find('by'):].replace('by','').strip()

                fandom['stories'].append(
                    {
                        'title': work.a.text.strip(),
                        'url': work.a.get('href'),
                        'fandoms': [tag.text.strip() for tag in fandom_tags],
                        'author': author_name
                    }
                )
            except Exception as error:
                print(error)
                print(f"{'title': work.a.text.strip()}\n{'url': work.a.get('href'),}")
                continue

        next_page = soup.find('li',{'class': 'next'}).a.get('href')
        url = f'https://archiveofourown.org/{next_page}'
        pp.pprint(fandom['stories'])
        print(f'Next url: {url}')
    except Exception as error:
        print(error)
        print(f'{url} was skipped')


for story in fandom['stories']:
    try:
        save_to_file(f'https://archiveofourown.org{story["url"]}')
    except Exception as e:
        print(f'ERROR! {story["url"]} was not saved.')
        print(e)
        continue

















#url = "https://archiveofourown.org/works/1005863?view_full_work=true"
def print_story(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    # Print title
    title_text = soup.title.text
    title = title_text.strip()
    # complete_work = open(title +".txt", "w")
    # complete_work.write(title + "\n\n")
    print(title + '\n')
    print(f'URL: {url} \n')
    print(f'Saved: {date.today()} \n')


    # Print stats
    stats_list = soup.find('dl', {'class': 'stats'})
    stats = stats_list.find_all(['dt','dd'])
    for stat in stats:
        text = stat.text.strip()
        #Put dt and dd tag text on the same line instead of new line
        if ":" in text:
            print(text, end=" ")

        else:
            print(text + "\n")


            #Remove stats row from meta data
            stats = soup.find_all(class_= "stats")
            for lines in stats:
                lines = lines.decompose()


                #Print meta data
                meta = soup.select('dl.work.meta.group')[0].find_all(['dt','dd'])
                for info in meta:
                    text = info.text.strip()
                    #Put dt and dd tag text on the same line instead of new line
                    if ":" in text:
                        print(text, end=" ")

                    else:
                        print(text + "\n")



                        #Print Summary
                        summary = soup.find('div', {'class':'summary'})
                        if summary:
                            text = summary.p.text.strip()
                            print(f'Summary:\n{text}\n')



                            #Main story text
                            chapters = soup.find('div',{'id':'chapters'})
                            tags = chapters.find_all(['h3','p','hr'])
                            for lines in tags:
                                #format spacing
                                if "\n" in lines:
                                    #print(lines.text)
                                    print(lines.text + "\n")
                                else:
                                    lines = lines.text + "\n"
                                    print(lines + "\n")




# fandom_category_links = []
# archives={}

# html = requests.get("https://archiveofourown.org/works/1005863?view_full_work=true")
#
# soup = BeautifulSoup(html.text, "html.parser")

# url = "https://archiveofourown.org/media"
# req = requests.get(url)
# soup = BeautifulSoup(req.text, 'html.parser')




# def get_fandom_links(link_list):
#     fandom_links = []
#     for url in link_list:
#         req = requests.get(url)
#         soup = BeautifulSoup(req.text, 'html.parser')
#
#         # get the category name
#         category_name = soup.title.text.strip()
#
#         # cleaning up the category name
#         category_name = category_name[:category_name.find('|')].strip()
#         # print(category_name)
#
#
#
#
#         # get alphabet fandom index list
#         alphabet_index = soup.select('li.letter.listbox.group')
#         for list_box in alphabet_index:
#             letter = list_box.h3.text.strip()
#             letter = letter[:letter.find('↑')].strip()
#             # print(letter)
#             letter = []
#             fandom_link_list = [f'https://archiveofourown.org/{link.get("href")}' for link in list_box.select('a.tag')]
#             # print(fandom_link_list[:5])
#             fandom_links.append(fandom_link_list)
#     print(fandom_links)
#     return fandom_links



# def get_fandom_category_links():
# # make a list fandom category links
#     fandom_category = soup.select('li.medium.listbox.group')
#     fandom_category_links = [f'https://archiveofourown.org/{cat.a.get("href")}' for cat in fandom_category]
#     print(fandom_category_links)
#
#     get_fandom_links(fandom_category_links)



# url = "https://archiveofourown.org/media/Anime%20*a*%20Manga/fandoms"
# req = requests.get(url)
# soup = BeautifulSoup(req.text, 'html.parser')
# #############################################
# alphabet_index = soup.select('li.letter.listbox.group')
# for list_box in alphabet_index:
#     letter = list_box.h3.text.strip()
#     letter = letter[:letter.find('↑')].strip()
#     print(letter)
#     link_list = [f'https://archiveofourown.org/{link.get("href")}' for link in list_box.select('a.tag')]
#     print(link_list[:5])
