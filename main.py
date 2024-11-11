import requests
from datetime import datetime, timezone
import smtplib
import time


MY_LAT = 24.5854 # Your latitude
MY_LONG = 73.7125 # Your longitude

# Fetch the ISS current position
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

# Email details
MY_EMAIL = "iampragnesh05@gmail.com"  # Replace with your email
MY_PASSWORD = "wcji vtlt mvsm qemr"  # Replace with your password
TO_EMAIL = "jobsforpragnesh@gmail.com"  # Replace with the recipient's email

# Function to send email notification
# Function to send email notification
def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        message = "Subject:Look Up!\n\nThe ISS is close to your position, and it’s currently dark. Look up!"
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=message.encode('utf-8')
        )



# Function to check ISS position and time
def check_iss_position():
    # Fetch the ISS current position
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # Extract ISS position and timestamp
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Check if the ISS is close to your position (within ±5 degrees)
    iss_close = (
        (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and
        (MY_LONG - 5 <= iss_longitude <= MY_LONG + 5)
    )

    # Fetch sunrise and sunset times
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Extract sunrise and sunset hours
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Current time in UTC
    current_hour = datetime.now(timezone.utc).hour

    # Check if it is currently dark (before sunrise or after sunset)
    is_dark = current_hour >= sunset_hour or current_hour <= sunrise_hour

    # If both conditions are met, send an email
    if iss_close and is_dark:
        send_email()
        print("Email sent! The ISS is close and it’s dark.")
    else:
        print("The ISS is either not close or it’s not dark.")

# Run the check every 60 seconds
while True:
    check_iss_position()
    time.sleep(60)  # Wait for 60 seconds before checking again