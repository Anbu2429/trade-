import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access the API

# --- NEW: Added a home route to fix the 404 error ---
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Online",
        "message": "Your Trading Backend is running perfectly!",
        "api_endpoint": "http://127.0.0.1:5000/api/candles?ticker=AAPL"
    })

# --- EXISTING: The main data route ---
@app.route('/api/candles', methods=['GET'])
def get_candle_data():
    ticker = request.args.get('ticker', 'AAPL')
    interval = request.args.get('interval', '1d')
    period = request.args.get('period', '1mo')
    
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        candles = []
        for index, row in df.iterrows():
            candles.append({
                "time": int(index.timestamp()),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2)
            })
        return jsonify(candles)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("Starting Trading Backend Server on port 5000...")
    app.run(port=5000, debug=True)