from flask import Flask, render_template_string, redirect, request, url_for
import os
import uuid
import requests
import json

app = Flask(__name__)

# This is your main page with the payment button
@app.route('/')
def index():
    # Generate a unique payment ID for this transaction
    payment_id = str(uuid.uuid4())
    
    # HTML directly embedded in the app.py file as requested
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CashApp $1 Payment Test</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
                line-height: 1.6;
            }
            .payment-button {
                background-color: #00D632;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 20px;
                font-weight: bold;
                transition: background-color 0.2s;
            }
            .payment-button:hover {
                background-color: #00C02E;
                transform: translateY(-1px);
            }
            .card {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-top: 30px;
            }
            h1 {
                color: #333;
                margin-bottom: 5px;
            }
            .price {
                font-size: 24px;
                font-weight: bold;
                color: #00D632;
                margin: 15px 0;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Test Payment</h1>
            <p>Simple test of your CashApp business integration</p>
            <div class="price">$1.00</div>
            <form action="/process_payment" method="post">
                <input type="hidden" name="payment_id" value="{{ payment_id }}">
                <input type="hidden" name="amount" value="1.00">
                <button type="submit" class="payment-button">Pay $1 with Cash App</button>
            </form>
        </div>
    </body>
    </html>
    '''
    
    # Render the HTML template with the payment_id
    return render_template_string(html, payment_id=payment_id)

# This route processes the payment when the button is clicked
@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_id = request.form.get('payment_id')
    amount = request.form.get('amount')
    
    # REPLACE THESE with your actual CashApp business credentials
    # You'll get these after signing up at https://developers.block.xyz/
    cashapp_client_id = "YOUR_CLIENT_ID"
    cashapp_api_key = "YOUR_API_KEY"
    
    # For testing without CashApp credentials, comment out the API code below
    # and uncomment this line to simulate a payment:
    return redirect(url_for('payment_success', payment_id=payment_id))
    
    # UNCOMMENT THIS SECTION once you have your CashApp API credentials
    """
    # CashApp API endpoint for creating payment requests
    api_url = "https://api.cash.app/payment-requests"
    
    # Create payment request payload according to CashApp API docs
    payload = {
        "amount": {
            "amount": amount,
            "currency": "USD"
        },
        "reference_id": payment_id,
        "redirect_url": request.url_root + "payment_success",
        "description": "Test $1 payment"
    }
    
    headers = {
        "Authorization": f"Bearer {cashapp_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()
        
        # Redirect to CashApp payment page
        return redirect(data["payment_url"])
    except Exception as e:
        return f"Payment error: {str(e)}", 500
    """

# This route handles successful payments
@app.route('/payment_success')
def payment_success():
    payment_id = request.args.get('payment_id')
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Success</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
                line-height: 1.6;
            }
            .success {
                color: #00D632;
                margin: 20px 0;
            }
            .card {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-top: 30px;
            }
            .check-icon {
                font-size: 48px;
                color: #00D632;
                margin-bottom: 15px;
            }
            .transaction {
                background-color: #f7f7f7;
                padding: 10px;
                border-radius: 4px;
                font-family: monospace;
                margin: 15px 0;
            }
            .btn {
                display: inline-block;
                background-color: #333;
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 4px;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="check-icon">✓</div>
            <h1 class="success">Payment Successful!</h1>
            <p>Thank you for your payment of $1.00</p>
            <div class="transaction">Transaction ID: {{ payment_id }}</div>
            <a href="/" class="btn">Return to payment page</a>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html, payment_id=payment_id)

# This route can be used for handling failed payments if needed
@app.route('/payment_failed')
def payment_failed():
    error = request.args.get('error', 'Unknown error')
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Failed</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }
            .failed {
                color: #e74c3c;
                margin: 20px 0;
            }
            .card {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 25px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-top: 30px;
            }
            .btn {
                display: inline-block;
                background-color: #333;
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 4px;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1 class="failed">Payment Failed</h1>
            <p>Sorry, we couldn't process your payment</p>
            <p>Error: {{ error }}</p>
            <a href="/" class="btn">Try Again</a>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html, error=error)

# Main entry point to run the application
if __name__ == '__main__':
    # Use the PORT environment variable provided by Render.com or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # In production (on Render.com), set debug to False
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
