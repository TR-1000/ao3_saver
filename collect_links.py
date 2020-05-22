import requests
import pprint
import time
pp = pprint.PrettyPrinter(indent=4)
from bs4 import BeautifulSoup
from datetime import date
from text_file_generator import save_to_file


# This script collects all links for a 'fandom', in this case the Star Wars Prequel Trilogy fandom. Because I love the Prequel Trilogy.

fandom = {
    'name': 'Star Wars Prequel Trilogy',
    'url': "https://archiveofourown.org/tags/Star%20Wars%20Prequel%20Trilogy/works?page=1&view_adult=true",
    'stories': []
}


url = "https://archiveofourown.org/tags/Star%20Wars%20Prequel%20Trilogy/works?page=4&view_adult=true"
while url:
    try:
        req = requests.get(url)
        print(f'Starting on {url}')
        time.sleep(6)
        soup = BeautifulSoup(req.text, "html.parser")
        works = soup.select('div.header.module')

        # Get link of each story on the page and save it with the save_to_file function.
        for work in works:
            try:
                time.sleep(7)
                story_url = f'https://archiveofourown.org/{work.a.get("href")}?view_full_work=true'
                save_to_file(story_url)
                print()

            except Exception as error:
                print(error)
                print('STORY WAS SKIPPED')
                continue

        # Create a dict with story information and append it to the list of stories in the fandom dict. I may refactor this to save the stories in a csv file first.

        # fandom_tags = work.select('h5 a')
        # try:
        #     author_name = work.find('a',{'rel':'author'}).text
        #     # If the author is anonymous or has no link this won't work
        # except:
        #     # This code finds the author name if it's not in an <a> tag
        #     by_line = work.h4.text.strip()
        #     author_name = by_line[by_line.find('by'):].replace('by','').strip()
        #
        # fandom['stories'].append(
        #     {
        #         'title': work.a.text.strip(),
        #         'url': work.a.get('href'),
        #         'fandoms': [tag.text.strip() for tag in fandom_tags],
        #         'author': author_name
        #     }
        # )

        # Get link to next page if it exists
        try:
            next_page = soup.find('li',{'class': 'next'}).a.get('href')
            url = f'https://archiveofourown.org/{next_page}'
        except:
            url = None
        print(f'Next url: {url}')

    # If there is an error saving the story skip to the next
    except Exception as error:
        print(error)
        print(f'PAGE SKIPPED\n{url}')



# Save stories from the fandom.['stories']
# for story in fandom['stories']:
#     try:
#         save_to_file(f'https://archiveofourown.org{story["url"]}?view_full_work=true&view_adult=true')
#     except Exception as e:
#         print(f'ERROR! {story["url"]} was not saved.')
#         print(e)
#         continue
