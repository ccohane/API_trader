from flask import Flask, jsonify, request, abort
import model

app=Flask(__name__)

@app.route("/balance/<apikey>", methods = ['GET'])
def get_balance(apikey):
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))
    return jsonify({"username":user_name, "balance": model.get_balance(user_name)})

@app.route("/quote/<apikey>", methods = ['POST'])
def get_quote(apikey):
    if not request.json or not 'Ticker' in request.json:
        abort(400)
    if not isinstance(request.json['Ticker'], (str)):
        abort(400)
    user_name=model.api_authenticate(apikey)

    if not user_name:
        return(jsonify({"error": "count not authenticate"}))
    ticker=request.json['Ticker']
    return jsonify({"Ticker": ticker, "price": model.quote(ticker)})

@app.route("/lookup/<apikey>", methods = ['POST'])
def get_lookup(apikey):
    if not request.json or not 'Company' in request.json:
        abort(400)
    if not isinstance(request.json['Company'], (str)):
        abort(400)
    
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))

    company=request.json['Company']
    return jsonify({"Ticker": model.lookup(company)})

@app.route("/buy/<apikey>", methods = ['POST'])
def get_buy(apikey):
    if not request.json or not 'Ticker' and 'Shares' in request.json:
        abort(400)
    if not isinstance(request.json['Ticker'], (str)):
        abort(400)
    if not isinstance(request.json['Shares'], (int)):
        abort(400)
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))
    ticker=request.json['Ticker']
    shares=request.json['Shares']
    return jsonify(model.buy(ticker,shares,user_name))

@app.route("/sell/<apikey>", methods = ['POST'])
def get_sell(apikey):
    if not request.json or not 'Ticker' and 'Shares' in request.json:
        abort(400)
    if not isinstance(request.json['Ticker'], (str)):
        abort(400)
    if not isinstance(request.json['Shares'], (int)):
        abort(400)
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))

    ticker=request.json['Ticker']
    shares=request.json['Shares']

    return jsonify(model.sell(ticker,shares,user_name))

@app.route("/deposit/<apikey>", methods = ['POST'])
def get_deposit( apikey):
    if not request.json or not 'Deposit' in request.json:
        abort(400)
    if not isinstance(request.json['Deposit'], (float,int)):
        abort(400)
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))
    money=request.json['Deposit']
    model.deposit(user_name,money)
    return jsonify({"username":user_name, "Deposit": money, "Balance": model.get_balance(user_name)})

@app.route("/holdings/<apikey>", methods = ['GET'])
def get_holdings(apikey):
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))
    
    return jsonify(model.print_holdings(user_name))

@app.route("/transactions/<apikey>", methods = ['GET'])
def get_transaction(apikey):
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))
    
    return jsonify(model.print_transactions(user_name))

@app.route("/dashboard/<apikey>", methods = ['GET'])
def get_dashboard(apikey):
    user_name=model.api_authenticate(apikey)
    if not user_name:
        return(jsonify({"error": "count not authenticate"}))
    return jsonify(model.dashboard(user_name))


if __name__=="__main__":
    app.run(debug=True)
