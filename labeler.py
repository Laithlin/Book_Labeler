# !/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar, FillingCirclesBar
import json
import urllib.parse
import checker

def search_lubimyczytac(books):
    book_url_dict = {}
    bar = Bar('Processing', max=len(books))
    for book in books:
        url = urllib.parse.urlunparse(('https', 'lubimyczytac.pl', '/szukaj/ksiazki', '', urllib.parse.urlencode({"phrase": book}), ""))
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        b_titles = soup.find_all("a", "authorAllBooks__singleTextTitle float-left")
        html_line = checker.find_title_match(b_titles, book)
        if html_line == "not found":
            print("Couldn't find book")
            book_url_dict[book] = "Couldn't find url"
            continue

        book_url_end = html_line.attrs.get('href')
        book_url = 'https://lubimyczytac.pl' + book_url_end
        book_category = get_book_category(book_url)
        book_url_dict[book] = [book_url, book_category]
        bar.next()
    bar.finish()
    return book_url_dict

def get_book_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_href = soup.find("a", "book__category d-sm-block d-none")
    category = category_href.get_text()
    return category

def create_file_for_books(data):
    with open("./data_for_books.json", "w", encoding='utf8') as outfile: 
        json.dump(data, outfile, ensure_ascii=False)

library = checker.get_books_names()
lib_url_cat = search_lubimyczytac(library)
print(lib_url_cat)
create_file_for_books(lib_url_cat)

