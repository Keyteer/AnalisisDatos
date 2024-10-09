import os
from bs4 import BeautifulSoup

folder_path = 'spam_archive'
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            file_content = file.read()

            soup = BeautifulSoup(file_content, 'lxml')
            paragraphs = soup.find_all("p")
            print("contenido del correo:")
            print(paragraphs)
