import os
import string
from collections import Counter
import bs4


def remove_headers(file):
    lines = file.readlines()
    content = []
    headers_ended = False
    for line in lines:
        if not headers_ended:
            if line.strip() == "":
                headers_ended = True
        else:
            if line.startswith(("Content-Type", "Content-Transfer-Encoding")) and content:
                content.pop()
            elif line.strip() != "" and line.strip() != "\n":
                    content.append(line)
    print(content)
    return "".join(content)

folder_path = "spam_archive"
not_content = []
errors = 0
counter = 0
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = remove_headers(file)
                stripped_text = bs4.BeautifulSoup(text, features="lxml").text.strip()
                #print(stripped_text)
                words = stripped_text.split()
                cleaned_words = []
                # tabla que cambia cualquier simbolo de puntuacion en string vacio
                trans_table = str.maketrans("", "", string.punctuation)
                for word in words:
                    cleaned_words.append(word.translate(trans_table).lower())
                print(cleaned_words)
                word_count = Counter(cleaned_words)
                print(word_count.most_common(10))
                counter +=1
                
        except UnicodeDecodeError:
            errors+=1
print(errors)
