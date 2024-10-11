import os
import string
import sys
from collections import Counter
import bs4
import base64
import unidecode
import csv
import nltk
from nltk.corpus import stopwords


def is_base64(file):
    file.seek(0)
    lines = file.readlines()
    for line in lines:
        if line.strip().startswith(("Content-Transfer-Encoding: base64", "Content-transfer-encoding: base64")):
            return True
    return False


def get_common_words(stripped_text):
    words = stripped_text.split()
    cleaned_words = []
    # tabla que cambia cualquier simbolo de puntuacion en string vacio
    trans_table = str.maketrans("", "", string.punctuation)
    for word in words:
        if not word.isascii():
            word = unidecode.unidecode(word)
        cleaned_words.append(word.translate(trans_table).lower())
    print(cleaned_words)
    word_count = Counter(cleaned_words)
    print(word_count.most_common(10))
    return word_count


def is_ignorable(file):
    file.seek(0)
    lines = file.readlines()
    for line in lines:
        if line.strip().startswith("Content-Type: text/plain; charset=ISO-2022-JP"):
            return True
    return False
def remove_headers(file):
    file.seek(0)
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
    #print(content)
    return "".join(content)

folder_path = "spam_archive"
not_content = []
errors = 0
counter = 0
words_top = Counter()
nltk.download('stopwords')
stopwords_set = set(stopwords.words('english'))

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        invalid_64 = False
        #try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            file.seek(0)
            if not is_ignorable(file):
                text = remove_headers(file)
                stripped_text = bs4.BeautifulSoup(text, features="lxml").text.strip()
                if is_base64(file):
                    print("yea it is")
                    missing_padding = len(stripped_text) % 4
                    try:
                        stripped_text = base64.b64decode(stripped_text + "="*(4-missing_padding)).decode("utf-8")
                    except ValueError as e:
                        invalid_64 = True
                        # quitar continue si se desea trabajar con correos en formato japones shift_jis
                        continue
                        try:
                            stripped_text = base64.b64decode(stripped_text + "=" * (4 - missing_padding)).decode("shift_jis")
                        except ValueError as e:
                            invalid_64=True
                            errors+=1
                            print(e)
                if not invalid_64:
                    words_top += get_common_words(stripped_text)
                    counter += 1
                else:
                    print("invalid 64")
            else:
                print("japo")

print(errors)
print("FINAL WORD TOP:")
words_top = words_top
words_top = Counter({word: count for word, count in words_top.items() if word not in stopwords_set}).most_common()

print(words_top)
with open('word_count.csv', mode='w', newline='') as ffile:
    writer = csv.writer(ffile)
    writer.writerow(['word', 'count'])
    writer.writerows(words_top)
sys.exit()
