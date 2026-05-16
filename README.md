# Italy Electricity Market Analysis

Analysis of Italian electricity spot prices (Zone South) using Python: 
EDA, volatility analysis, and price forecasting with SARIMA and XGBoost.

## Project Overview

This project analyzes hourly electricity spot prices from the Italian 
Power Exchange (GME) for the Southern bidding zone (Zone South) in 2025. 
It covers the full pipeline from raw data to forecasting models, 
with a focus on quantitative methods applied to energy markets.

## Data

- **Source:** GME - Gestore dei Mercati Energetici (mercatoelettrico.org)
- **Market:** MGP (Mercato del Giorno Prima) - Day-Ahead Market
- **Zone:** Sud (Southern Italy)
- **Period:** January - December 2025
- **Granularity:** Hourly prices (€/MWh)

## Project Structure
│
├── 01_load_data.py        # Data loading and cleaning
├── 02_eda.py              # Exploratory Data Analysis
├── 03_volatility.py       # Volatility and returns analysis
├── 04_forecasting.py      # SARIMA model (24h forecast)
├── 05_xgboost.py          # XGBoost model (7-day forecast)
└── README.md

## Key Findings

- **Winter premium:** January and February show the highest average 
  prices due to heating demand and low solar production
- **Duck curve effect:** High price volatility in May and June driven by 
  excess solar generation in midday hours followed by sharp evening ramps
- **Daylight saving anomaly:** Artificial volatility spike around 
  October 27 due to clock change — handled via data cleaning
- **Lag-24 dominance:** The most predictive feature is the price 
  from the same hour the previous day (50% feature importance in XGBoost)

## Models

| Model   | Forecast Horizon | MAE        |
|---------|-----------------|-------------|
| SARIMA  | 24 hours        | 4.53 €/MWh  |
| XGBoost | 7 days          | 8.30 €/MWh  |

## Technologies

- Python 3.11
- pandas, numpy, matplotlib, seaborn
- statsmodels (SARIMA)
- XGBoost, scikit-learn

## How to Run

1. Download hourly zonal prices from [GME website](https://www.mercatoelettrico.org)
2. Place Excel files in the `dataSUD/` folder
3. Run scripts in order: `ExcelFiles.py` → `XGboost.py`

## Author

Paolo — MSc Energy Engineering, Politecnico di Milano