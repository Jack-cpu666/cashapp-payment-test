import requests
import json

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_id = request.form.get('payment_id')
    amount = request.form.get('amount')
    
    # Replace with your actual CashApp credentials
    cashapp_client_id = "YOUR_CLIENT_ID"
    cashapp_api_key = "YOUR_API_KEY"
    
    # CashApp API endpoint
    api_url = "https://api.cash.app/payment-requests"
    
    # Create payment request
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
