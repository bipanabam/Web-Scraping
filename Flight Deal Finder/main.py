from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LON"
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()


# # Adding users
# print("Welcome to Avenger's Flight Club!")
# print("We find the best flight deal for you and email you.")
# first_name = input("What is your first name?\n")
# last_name = input("What is our last name?\n")
# email1 = input("What is your email?\n")
# email2 = input("Type your email again.\n")
# if email1 == email2:
#     user = data_manager.add_customer(first_name, last_name, email2)
#     print(user)
#     if user:
#         print("You're in the club!")
# else:
#     print("Email does not match. Try again!")


sheet_data = data_manager.get_destination_data()
# print(sheet_data)
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(ORIGIN_CITY_IATA,
                                         destination["iataCode"],
                                         from_time=tomorrow,
                                         to_time=six_month_from_today)
    if flight.price < destination["lowestPrice"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} " \
                  f"to {flight.destination_city}-{flight.destination_airport}, " \
                  f"from {flight.out_date} to {flight.return_date}."

        notification_manager.send_mail(emails, message)
