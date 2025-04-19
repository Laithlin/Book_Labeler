import os
from unidecode import unidecode
from progress.bar import Bar, FillingCirclesBar

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
            title_unidecode = unidecode(title.get_text())
            if title_unidecode[0] == ' ':
                title_unidecode = title_unidecode[1:-1]
            if title_unidecode in unidecode(book):
                return title
    return "not found"