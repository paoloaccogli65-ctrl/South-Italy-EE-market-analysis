import pandas as pd
import os
import glob

data_folder = r"C:\Users\paolo\OneDrive\Desktop\EnergyProject\dataSUD"

all_files = glob.glob(os.path.join(data_folder, "*.xlsx"))

dfs = []
for f in all_files:
    df = pd.read_excel(f, decimal=',')
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

df.columns = ['data', 'ora', 'prezzo']

df['datetime'] = pd.to_datetime(df['data'], dayfirst=True) + pd.to_timedelta(df['ora'] - 1, unit='h')

df = df.sort_values('datetime').reset_index(drop=True)
df = df[['datetime', 'prezzo']]

print(df.head(10))
print(f"\nTotale righe: {len(df)}")
print(f"Da: {df['datetime'].min()}")
print(f"A:  {df['datetime'].max()}")
print(f"\nPrezzo medio: {df['prezzo'].mean():.2f} €/MWh")
print(f"Prezzo min:   {df['prezzo'].min():.2f} €/MWh")
print(f"Prezzo max:   {df['prezzo'].max():.2f} €/MWh")

df.to_csv(r"C:\Users\paolo\OneDrive\Desktop\EnergyProject\dataSUD\prezzi_sud_2025.csv", 
          index=False, sep=';')
print("\nFile CSV salvato!")