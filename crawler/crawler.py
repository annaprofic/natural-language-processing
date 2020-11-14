from bs4 import BeautifulSoup
import requests
import re


def parse(page_url):
    page_content = BeautifulSoup(page_url.content, 'lxml')

    title = page_content.find('h1', {'class': 'firstHeading'}).text

    content_list = page_content.find_all('span', {'class': 'mw-headline'})
    content = ''
    for content_item in content_list:
        content += content_item.text + ' '

    all_content = page_content.find('div', {'class': 'mw-content-ltr'}).text

    return title, content, all_content


def categories_search(start_url):
    page_content = BeautifulSoup(start_url.content, 'lxml')
    categories_set = set(re.findall(r'Wikipedia:Contents/\w+', str(page_content.find_all('a'))))
    return [category.split("Wikipedia:Contents/")[1] for category in categories_set]


def run_parsing_for_category(category_name):
    data = {'article title': '', 'content list': '', 'all content': ''}

    # PARSING
    for i in range(0, 201):
        base_url = requests.get('https://en.wikipedia.org/wiki/Special:Random?Category=' + category_name, timeout=5)
        article_title, content, all_content = parse(base_url)
        data["article title"] += " ".join(re.split("\s+", article_title + ' ', flags=re.UNICODE)) if not None else ''
        data["content list"] += " ".join(re.split("\s+", content + ' ', flags=re.UNICODE)) if not None else ''
        data["all content"] += " ".join(re.split("\s+", all_content + ' ', flags=re.UNICODE)) if not None else ''

    f = open('./output/category_' + category_name + '.txt', "w+")
    for k, v in data.items():
        f.write('__________________________' + str(k) + '__________________________\n' +
                str(v) + '\n')
    f.close()


if __name__ == "__main__":

    start_page = requests.get('https://en.wikipedia.org/wiki/Wikipedia:Contents', timeout=5)
    categories = categories_search(start_page)
    print("Available categories:", categories)

    if 'History' in categories:
        run_parsing_for_category('History')
    if 'Society' in categories:
        run_parsing_for_category('Society')
    if 'Technology' in categories:
        run_parsing_for_category('Technology')
    if 'Human_activities' in categories:
        run_parsing_for_category('Human_activities')

    # uncomment if want to check all categories:

    # for category in categories:
    #     run_parsing_for_category(category)
