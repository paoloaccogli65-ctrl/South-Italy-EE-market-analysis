import pandas as pd
import matplotlib.pyplot as plt

# 1. Carica dati
df = pd.read_csv(r"C:\Users\paolo\OneDrive\Desktop\EnergyProject\data\prezzi_sud_2025.csv",
                 sep=';', parse_dates=['datetime'])

# 2. Rimuove prezzi anomali
df = df[df['prezzo'] > 1].reset_index(drop=True)

# 3. Calcola rendimenti
df['return'] = df['prezzo'].pct_change() * 100

# 4. Winsorizing (limitiamo rendimenti estremi dovuti alla duck curve)
q99 = df['return'].quantile(0.99)
q01 = df['return'].quantile(0.01)
df['return'] = df['return'].clip(lower=q01, upper=q99)

# 5. Escludo cambio ora legale, crea anomalia
mask = (df['datetime'] >= '2025-10-25') & (df['datetime'] <= '2025-10-30')
df = df[~mask].reset_index(drop=True)

# 6. Volatilità rolling
df['volatility_7d'] = df['return'].rolling(window=168).std()

# --- Grafici ---
plt.figure(figsize=(14, 4))
plt.plot(df['datetime'], df['return'], linewidth=0.5, alpha=0.7, color='steelblue')
plt.axhline(0, color='black', linewidth=0.8)
plt.title('Rendimenti orari - Zona Sud 2025')
plt.ylabel('Variazione %')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 4))
plt.plot(df['datetime'], df['volatility_7d'], linewidth=1, color='coral')
plt.title('Volatilità rolling 7 giorni')
plt.ylabel('Deviazione standard rendimenti %')
plt.tight_layout()
plt.show()