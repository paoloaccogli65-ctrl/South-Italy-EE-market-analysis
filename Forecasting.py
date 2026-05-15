import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

# Carica dati
df = pd.read_csv(r"C:\Users\paolo\OneDrive\Desktop\EnergyProject\data\prezzi_sud_2025.csv",
                 sep=';', parse_dates=['datetime'])

df = df[df['prezzo'] > 1].reset_index(drop=True)
df = df.set_index('datetime')

# Usa solo gli ultimi 30 giorni per velocità
df_model = df['prezzo']['2025-12-01':]
# Split train/test - ultimi 24 ore come test
train = df_model[:-24]
test  = df_model[-24:]

# Modello SARIMA con stagionalità giornaliera (24 ore)
model = SARIMAX(train, 
                order=(1, 0, 1),           # p, d, q
                seasonal_order=(1, 0, 1, 24))  # stagionalità 24 ore

print("Training del modello in corso...")
result = model.fit(disp=False)

# Previsione 24 ore
forecast = result.forecast(steps=24)

# Grafico
plt.figure(figsize=(14, 5))
plt.plot(train[-72:].index, train[-72:], label='Storico', color='steelblue')
plt.plot(test.index, test, label='Reale', color='green')
plt.plot(test.index, forecast, label='Previsione', color='coral', linestyle='--')
plt.title('Previsione prezzi 24 ore - Zona Sud')
plt.ylabel('€/MWh')
plt.legend()
plt.tight_layout()
plt.show()

# Errore
mae = abs(test - forecast).mean()
print(f"MAE: {mae:.2f} €/MWh")