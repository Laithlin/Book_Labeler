# !/usr/bin/python3
import os

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

# to search
# query = "Geeksforgeeks"

# for j in search(query, tld="co.in", num=10, stop=10, pause=2):
#     print(j)

path_to_books = "/home/justyna/ksiegarnia/test/"


directory_list = list()
for root, dirs, files in os.walk(path_to_books, topdown=False):
    print(files)
    for name in dirs:
        directory_list.append(name)
        os.path.join(root, name)

print(directory_list)
