from bs4 import BeautifulSoup
import requests

base_url = requests.get('https://en.wikipedia.org/wiki/Special:Random', timeout=5)


def parse(page_url):
    page_content = BeautifulSoup(page_url.content, 'lxml')

    article_title = page_content.find('h1', {'class': 'firstHeading'}).text
    print("title: ", article_title)

    content_list = page_content.find_all('span', {'class': 'mw-headline'})
    content = ''
    if content_list is not None:
        for content_item in content_list:
            content += content_item.text

    print("content: ", content)
    references_list = page_content.find_all('span', {'class': 'reference-text'})
    references = ''
    for reference in references_list:
        references += reference.text

    print("references: ", references)
    last_edition = page_content.find('li', {'id': 'footer-info-lastmod'}).text

    categories = page_content.find('div', {'class': 'mw-normal-catlinks'}).ul.text
    print("categories: ", categories)

    all_content = page_content.find('div', {'class': 'mw-content-ltr'}).text
    print("All content: ", all_content.replace('\n', ''))


if __name__ == "__main__":
    data = dict()
    parse(base_url)


