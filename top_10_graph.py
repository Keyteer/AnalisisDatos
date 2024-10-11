import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("word_count.csv")
top_10_palabras = df.sort_values(by='count', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x='word', y='count', data=top_10_palabras)
plt.title('10 Palabras más frecuentes en correos tipo spam')
plt.xlabel('Palabra')
plt.ylabel('Conteo')
plt.xticks(rotation=45)
plt.show()
