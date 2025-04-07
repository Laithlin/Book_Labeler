# !/usr/bin/python3
import os
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar, FillingCirclesBar
import json
import urllib.parse
from unidecode import unidecode

def cut_extension(file):
    ext_len = check_extension(file)
    return file[:(len(file) - ext_len)]

def check_extension(file):
    # default is pdf, 4 symbols ".pdf"
    extension_len = 4
    ext = file[len(file)-4:len(file)]
    if(ext == "mobi" or ext == "epub"):
        extension_len = 5
    return extension_len\

def check_rtf_doc_extensions_number(extension):
    if(extension == ".rtf" or extension == "docx" or extension == ".doc"):
        print(extension)
        return True

def get_books_names():
    path_to_books = "/home/justyna/ksiegarnia/Ebooki/"
    bar = Bar('Processing', max=len(os.listdir(path_to_books)))
    books = list()
    for _, _, files in os.walk(path_to_books, topdown=False):
        for file in files:
            books.append(cut_extension(file))
        bar.next()

    bar.finish()
    return books

def find_title_match(books_titles, book):
    for title in books_titles:
            # print(title.get_text())
            title_unidecode = unidecode(title.get_text())
            if title_unidecode[0] == ' ':
                title_unidecode = title_unidecode[1:-1]
            # print(title_unidecode)
            # print(unidecode(book))
            if title_unidecode in unidecode(book):
                # print("jest")
                return title
    return "not found"

def search_lubimyczytac(books):
    book_url_dict = {}
    bar = Bar('Processing', max=len(books))
    for book in books:
        url = urllib.parse.urlunparse(('https', 'lubimyczytac.pl', '/szukaj/ksiazki', '', urllib.parse.urlencode({"phrase": book}), ""))
        # print(url)
        # print(book)
        res = requests.get(url)
        # print(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        b_titles = soup.find_all("a", "authorAllBooks__singleTextTitle float-left")
        html_line = find_title_match(b_titles, book)
        if html_line == "not found":
            print("Couldn't find book")
            book_url_dict[book] = "Couldn't find url"
            continue
        # print(str(html_line))
        # print(html_line.attrs.get('href'))
        book_url_end = html_line.attrs.get('href')
        # print(str(html_line.get('href')))
        # print(book_url_end)
        book_url = 'https://lubimyczytac.pl' + book_url_end
        # print(book_url)
        book_category = get_book_category(book_url)
        # print(book_category)
        book_url_dict[book] = [book_url, book_category]
        bar.next()
    bar.finish()
    return book_url_dict

def get_book_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_href = soup.find("a", "book__category d-sm-block d-none")
    # print(category_href)
    category = category_href.get_text()
    # print(category)
    return category

def create_file_for_books(data):
    with open("./data_for_books.json", "w", encoding='utf8') as outfile: 
        json.dump(data, outfile, ensure_ascii=False)

library = get_books_names()
lib_url_cat = search_lubimyczytac(library)
print(lib_url_cat)
create_file_for_books(lib_url_cat)

