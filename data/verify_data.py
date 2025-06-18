import pandas as pd

df = pd.read_csv("housing_clean.csv")

''' ce script sert à verifier que les données sont nettoyées '''

print(df.head())
print(df.isnull().sum())
print(df.columns)
print(df.shape)         
print(df.describe())    
