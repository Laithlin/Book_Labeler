# !/usr/bin/python3
import os
import requests
from bs4 import BeautifulSoup

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
    path_to_books = "/home/justyna/ksiegarnia/test/"

    books = list()
    for root, dirs, files in os.walk(path_to_books, topdown=False):
        for file in files:
            # print(file)
            books.append(cut_extension(file) + " lubimyczytac")

    return books

def search_in_google(books):
    urls = []
    for book in books:
        for j in search(book, tld="co.in", num=2, stop=2, pause=5):
            # print(j)
            urls.append(j)
    return urls

# to search
# query = "Geeksforgeeks"

# for j in search(query, tld="co.in", num=10, stop=10, pause=2):
#     print(j)


library = get_books_names()
# print(library[0])
url = search_in_google([library[0]])
response = requests.get(url[0])
# print(response.text)
# print(url)
# print(directory_list)
# print("Files:")
# print(library)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.find_all("a", "book__category d-sm-block d-none"))
# try:
#     with open("./file.txt", "x") as f:
#         f.write(response.text)
# except FileExistsError:
#     print("Already exists.")



