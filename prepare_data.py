import pandas as pd
import os

#Loading dataset
df = pd.read_csv("data/housing_raw.csv")

df.dropna(inplace=True) #Delete lines with missing columns
df.drop(columns=["ocean_proximity"], inplace=True) # Supprimer la colonne catégorielle

#Creating new features
df["rooms_per_household"] = df["total_rooms"] / df["households"]
df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"]
df["population_per_household"] = df["population"] / df["households"]

#delete original columns
df.drop(columns=["total_rooms", "total_bedrooms", "population", "households"], inplace=True)

#save the result
os.makedirs("data", exist_ok=True)
df.to_csv("data/housing_clean.csv", index=False)

print("Clean data saved in  'data/housing_clean.csv'")
print(df.head()) # pour afficher les premieres lignes afin de s'assurer que le dataset est bien
