import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica dati
df = pd.read_csv(r"C:\Users\paolo\OneDrive\Desktop\EnergyProject\data\prezzi_sud_2025.csv", 
                 sep=';', parse_dates=['datetime'])

# Aggiungi colonne utili
df['ora']     = df['datetime'].dt.hour
df['mese']    = df['datetime'].dt.month
df['giorno']  = df['datetime'].dt.dayofweek  # 0=lunedì, 6=domenica
df['weekend'] = df['giorno'] >= 5

# --- Grafico 1: prezzi nel tempo ---
plt.figure(figsize=(14, 4))
plt.plot(df['datetime'], df['prezzo'], linewidth=0.5, alpha=0.8)
plt.title('Prezzi elettricità - Zona Sud 2025')
plt.ylabel('€/MWh')
plt.tight_layout()
plt.show()

# --- Grafico 2: prezzo medio per ora del giorno ---
plt.figure(figsize=(10, 4))
df.groupby('ora')['prezzo'].mean().plot(kind='bar', color='steelblue')
plt.title('Prezzo medio per ora del giorno')
plt.xlabel('Ora')
plt.ylabel('€/MWh')
plt.tight_layout()
plt.show()

# --- Grafico 3: prezzo medio per mese ---
plt.figure(figsize=(10, 4))
df.groupby('mese')['prezzo'].mean().plot(kind='bar', color='coral')
plt.title('Prezzo medio per mese')
plt.xlabel('Mese')
plt.ylabel('€/MWh')
plt.tight_layout()
plt.show()

# --- Grafico 4: heatmap ora x mese ---
pivot = df.pivot_table(values='prezzo', index='ora', columns='mese', aggfunc='mean')

plt.figure(figsize=(12, 6))
sns.heatmap(pivot, cmap='RdYlGn_r', annot=False, fmt='.0f', linewidths=0.5)
plt.title('Prezzo medio €/MWh - Ora vs Mese')
plt.xlabel('Mese')
plt.ylabel('Ora del giorno')
plt.tight_layout()
plt.show()