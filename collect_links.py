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

                break
            except Exception as error:
                print(error)
                print(f"{'title': work.a.text.strip()}\n{'url': work.a.get('href'),}")
                continue

        next_page = soup.find('li',{'class': 'next'}).a.get('href')
        url = f'https://archiveofourown.org/{next_page}'
        pp.pprint(fandom['stories'])
        print(f'Next url: {url}')
        break
    except Exception as error:
        print(error)
        print(f'{url} was skipped')


for story in fandom['stories']:
    try:
        save_to_file(f'https://archiveofourown.org{story["url"]}?view_full_work=true&view_adult=true')
    except Exception as e:
        print(f'ERROR! {story["url"]} was not saved.')
        print(e)
        continue
