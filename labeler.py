# !/usr/bin/python3
import os

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

def cut_extension(file):
    check_extension(file)
    file_len = len(file)
    return file[:(file_len - 4)]

def check_extension(file):
    # default is pdf, 4 symbols ".pdf"
    is_rtf_doc_or_docx = False
    extension_len = 4
    ext = file[len(file)-4:len(file)]
    # print(extension)
    is_rtf_doc_or_docx = check_rtf_doc_extensions_number(ext)

    if(is_rtf_doc_or_docx):
        print(file)

def check_rtf_doc_extensions_number(extension):
    if(extension == ".rtf" or extension == "docx" or extension == ".doc"):
        print(extension)
        return True

def get_books_names():
    # path_to_books = "/home/justyna/ksiegarnia/test/"
    path_to_books = "/home/justyna/ksiegarnia/Ebooki/"

    books = list()
    # directory_list = list()
    for root, dirs, files in os.walk(path_to_books, topdown=False):
        for file in files:
            # print(file)
            books.append(cut_extension(file))
        # print(files)
        # for name in dirs:
        #     directory_list.append(name)
        #     os.path.join(root, name)
    return books

def search_in_google(books):
    for book in books:
        for j in search(book, tld="co.in", num=10, stop=10, pause=2):
            print(j)

# to search
# query = "Geeksforgeeks"

# for j in search(query, tld="co.in", num=10, stop=10, pause=2):
#     print(j)


library = get_books_names()
# print(directory_list)
# print("Files:")
# print(library)



