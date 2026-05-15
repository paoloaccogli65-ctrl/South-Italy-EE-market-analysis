import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Carica dati
df = pd.read_csv(r"C:\Users\paolo\OneDrive\Desktop\EnergyProject\data\prezzi_sud_2025.csv",
                 sep=';', parse_dates=['datetime'])

df = df[df['prezzo'] > 1].reset_index(drop=True)

# --- Feature Engineering ---
df['ora']          = df['datetime'].dt.hour
df['giorno']       = df['datetime'].dt.dayofweek
df['mese']         = df['datetime'].dt.month
df['weekend']      = (df['giorno'] >= 5).astype(int)
df['festivo']      = df['datetime'].dt.date.astype(str).isin([
                        '2025-01-01', '2025-04-25', '2025-05-01',
                        '2025-08-15', '2025-11-01', '2025-12-25', '2025-12-31'
                     ]).astype(int)

# Lag features - prezzi delle ore precedenti
df['lag_24']  = df['prezzo'].shift(24)   # stesso momento ieri
df['lag_48']  = df['prezzo'].shift(48)   # stesso momento 2 giorni fa
df['lag_168'] = df['prezzo'].shift(168)  # stesso momento settimana scorsa

# Media mobile
df['rolling_24'] = df['prezzo'].shift(1).rolling(24).mean()

# Rimuovi righe con NaN
df = df.dropna().reset_index(drop=True)

# --- Split train/test ---
# Train: tutto tranne ultimi 7 giorni
# Test: ultimi 7 giorni
split = len(df) - 24*7
train = df[:split]
test  = df[split:]

features = ['ora', 'giorno', 'mese', 'weekend', 'festivo',
            'lag_24', 'lag_48', 'lag_168', 'rolling_24']

X_train = train[features]
y_train = train['prezzo']
X_test  = test[features]
y_test  = test['prezzo']

# --- Modello ---
model = XGBRegressor(n_estimators=500, learning_rate=0.05, 
                     max_depth=6, random_state=42)
print("Training XGBoost...")
model.fit(X_train, y_train)

# --- Previsione ---
forecast = model.predict(X_test)
mae = mean_absolute_error(y_test, forecast)
print(f"MAE: {mae:.2f} €/MWh")

# --- Grafico ---
plt.figure(figsize=(14, 5))
plt.plot(test['datetime'], y_test.values, label='Reale', color='green')
plt.plot(test['datetime'], forecast, label='Previsione', color='coral', linestyle='--')
plt.title('Previsione prezzi 7 giorni - XGBoost - Zona Sud')
plt.ylabel('€/MWh')
plt.legend()
plt.tight_layout()
plt.show()

# --- Feature importance ---
plt.figure(figsize=(8, 5))
pd.Series(model.feature_importances_, index=features).sort_values().plot(kind='barh', color='steelblue')
plt.title('Feature Importance')
plt.tight_layout()
plt.show()