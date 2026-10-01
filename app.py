from flask import Flask, request, jsonify
import pandas as pd
import ta


app = Flask(__name__)

def analyze_trade_signal(df, strategy):
    """
    Evaluates market conditions using Technical Indicators to decide WHY a trade is taken.
    """
    df['EMA_FAST'] = ta.ema(df['close'], length=9)
    df['EMA_SLOW'] = ta.ema(df['close'], length=21)
    df['RSI'] = ta.rsi(df['close'], length=14)

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    signal = None
    reason = "No trade signal detected."

    if strategy == 'ema_cross':
        if prev_row['EMA_FAST'] < prev_row['EMA_SLOW'] and last_row['EMA_FAST'] > last_row['EMA_SLOW']:
            signal = 'BUY'
            reason = "Bullish EMA Crossover: Fast EMA (9) crossed above Slow EMA (21)."
        elif prev_row['EMA_FAST'] > prev_row['EMA_SLOW'] and last_row['EMA_FAST'] < last_row['EMA_SLOW']:
            signal = 'SELL'
            reason = "Bearish EMA Crossover: Fast EMA (9) crossed below Slow EMA (21)."

    elif strategy == 'rsi_ema':
        if last_row['close'] > last_row['EMA_SLOW'] and last_row['RSI'] < 30:
            signal = 'BUY'
            reason = "RSI Oversold (<30) while price is trading above Slow EMA (21)."
        elif last_row['close'] < last_row['EMA_SLOW'] and last_row['RSI'] > 70:
            signal = 'SELL'
            reason = "RSI Overbought (>70) while price is trading below Slow EMA (21)."

    return signal, reason

@app.route('/start-bot', methods=['POST'])
def start_bot():
    try:
        data = request.form
        token = data.get('metaapi_token')
        account_id = data.get('account_id')
        trading_style = data.get('trading_style')
        strategy = data.get('strategy')
        lot_size = data.get('lot_size')
        stop_loss = data.get('stop_loss')
        take_profit = data.get('take_profit')
        trailing_stop = data.get('trailing_stop')

        # Log details to console
        print(f"[BOT STARTED] Account: {account_id} | Style: {trading_style} | Strategy: {strategy}")
        print(f"[RISK MANAGEMENT] Lot: {lot_size} | SL: {stop_loss} pips | TP: {take_profit} pips | Trailing SL: {trailing_stop} pips")

        return jsonify({
            "status": "success",
            "message": f"Trading Bot successfully started for Account {account_id} using {strategy.upper()} strategy."
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    return jsonify({
        "status": "success",
        "message": "Trading Bot has been stopped successfully."
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
