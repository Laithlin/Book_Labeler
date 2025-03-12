# !/usr/bin/python3
import os
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar, FillingCirclesBar
import json
import urllib.parse

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

def cut_extension(file):
    ext_len = check_extension(file)
    return file[:(len(file) - ext_len)]

def check_extension(file):
    # default is pdf, 4 symbols ".pdf"
    extension_len = 4
    ext = file[len(file)-4:len(file)]
    if(ext == "mobi" or ext == "epub"):
        extension_len = 5

    return extension_len
def check_rtf_doc_extensions_number(extension):
    if(extension == ".rtf" or extension == "docx" or extension == ".doc"):
        print(extension)
        return True

def get_books_names():
    path_to_books = "/home/justyna/ksiegarnia/test_one_book/"
    # files = os.listdir(path_to_books)
    bar = Bar('Processing', max=len(os.listdir(path_to_books)))
    # print(len(files))
    books = list()
    for _, _, files in os.walk(path_to_books, topdown=False):
        for file in files:
            # print(file)
            # books.append(cut_extension(file) + " lubimyczytac")
            books.append(cut_extension(file))
        bar.next()

    bar.finish()
    return books

def search_in_google(books):
    urls = []
    unable_to_find = []
    lib = {}
    bar = FillingCirclesBar('Processing', max=len(books))
    for book in books:
        start_url_len = len(urls)

        for j in search(book, tld="co.in", num=3, stop=3, pause=5):
            if(check_url(j)):
                urls.append(j)
            continue

        end_url_len = len(urls)
        if(start_url_len == end_url_len):
            unable_to_find.append(book)
            print("didn't find good url")
            urls.append("didn't find good url")
        lib[book] = urls[-1]
        bar.next()
    bar.finish()
    return urls, lib

def search_in_bing(books):
    for book in books:
        query = book.replace(" ", "+")
        # url = urlunparse(("https", "www.bing.com", "/search", "", urlencode({"q": query}), ""))
        url = urllib.parse.urlunparse(('https', 'bing.com', '/search', '', urllib.parse.urlencode({"q": book}), ""))
        # print(query)
        print(url)
        custom_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        res = requests.get(url, headers={"User-Agent": custom_user_agent})

        # print(res.status_code)
        # print(res.text)
        # # print(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        urls = soup.find_all("a")
        # print(urls)
        for link in urls:
            # print(link.get('href'))
            if(check_url(link.get('href'))):
                print(link.get('href'))

def search_lubimyczytac(books): 
    for book in books:
        url = urllib.parse.urlunparse(('https', 'lubimyczytac.pl', '/szukaj/ksiazki', '', urllib.parse.urlencode({"phrase": book}), ""))
        print(url)
        res = requests.get(url)
        # print(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        urls = soup.find_all("a")
        # print(urls)
        for link in urls:
            link_href = link.get('href')
            if(link_href == None):
                print(link_href)
            else:
                # print(link_href + " check")
                check_url(link_href)
            # if(check_url(link.get('href'))):
            #     print(link.get('href'))

# TODO stworzyc oddzielna funkcje do wyciagania tytulu ksiazki
# jak bede miala tytul to latwo wyszukac odpowiedni url

# TODO zrobic porzadek w kodzie bo juz sie gubie co jest od czego

def check_url(url):
    # print(url)
    # contain_string = "https://lubimyczytac.pl/ksiazka/"
    contain_string = "/ksiazka/"
    if contain_string in url:
        print(url)
        return True
    return False

def get_book_category(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    category_href = soup.find("a", "book__category d-sm-block d-none")
    # print(category_href)
    category = category_href.get_text()
    print(category)

def create_file_for_links(data):
    with open("./url_for_books.json", "w", encoding='utf8') as outfile: 
        json.dump(data, outfile, ensure_ascii=False)

library = get_books_names()
search_lubimyczytac(library)
# # print(library[0])
# search_in_bing(library)
# url, lib = search_in_google(library)
# print(lib)
# create_file_for_links(lib)
# print("linki:\n")
# print(url)
# res = requests.get(url[0])

# get_book_category(res)

