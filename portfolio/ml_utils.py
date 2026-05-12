import yfinance as yf
import datetime as dt
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_price(ticker_symbol):
    try:
        data = yf.download(ticker_symbol, period="60d", interval="1d")
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
        if data.empty:
            return None
            
        data = data[['Close']].reset_index()
        
        data['Date_Ordinal'] = data['Date'].map(dt.datetime.toordinal)
        
        X = data[['Date_Ordinal']].values
        y = data['Close'].values

        model = LinearRegression()
        model.fit(X, y)
        
        today_ordinal = dt.date.today().toordinal()

        # Predict using that ordinal
        prediction = model.predict([[today_ordinal]])
                
        return round(float(prediction[0]), 2)
    except Exception:
        return None