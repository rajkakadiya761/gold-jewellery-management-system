import requests

def make_gapi_request():
    # api_key = "goldapi-4fdjs3fsm6es0363-io"
    api_key = "goldapi-jti2sm6dzkgyp-io"
    metals = ["XAU", "XAG", "XPT"]  # Gold, Silver, Platinum
    curr = "INR"
    prices = {}

    for metal in metals:
        url = f"https://www.goldapi.io/api/{metal}/{curr}"
        
        headers = {
            "x-access-token": api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # Get the price for 1 gram (if available) or price field in INR
            price_per_gram = result.get('price_gram_24k') if metal == "XAU" else result.get('price')
            prices[metal] = round(price_per_gram, 2) if price_per_gram else "Data Unavailable"

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {metal} price:", str(e))
            prices[metal] = "Error"

    return prices

# Example usage
prices = make_gapi_request()
print(f"Gold Price: ₹{prices.get('XAU', 'Error')} /gram")
print(f"Silver Price: ₹{prices.get('XAG', 'Error')} /gram")
print(f"Platinum Price: ₹{prices.get('XPT', 'Error')} /gram")
