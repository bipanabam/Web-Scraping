import requests

SHEETY_USERS_ENDPOINT = "https://api.sheety.co/dd83498eaa8c93dad4326952505dbf48/flightDeals/users"
SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/dd83498eaa8c93dad4326952505dbf48/flightDeals/prices"
TOKEN = "your-sheety-prices-token"
headers = {
            "Authorization": f"Basic {TOKEN}"
        }


class DataManager:
    """Responsible for talking to the Google Sheet: Flight Deal(users & prices)"""
    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_data, headers=headers)
            response.raise_for_status()

    def get_customer_emails(self):
        customers_endpoint = SHEETY_USERS_ENDPOINT
        response = requests.get(url=customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data

    def add_customer(self, first_name, last_name, email):
        customers_endpoint = SHEETY_USERS_ENDPOINT
        data = {
                "user": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email
                }
        }
        response = requests.post(url=customers_endpoint, json=data)
        data = response.json()
        return data

