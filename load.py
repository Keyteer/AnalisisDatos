import pandas as pd

df = pd.read_csv("./mails/spam_assassin.csv")

N_rows = df.shape[0]
mean_length = df['text'].apply(len).mean()

print(f"Number of rows: {N_rows}")
print(f"Mean length of text: {mean_length}")

for row in df.iterrows():
    for word in row[1]['text'].split():
        print(word)
        break