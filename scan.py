import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Constants
URL = "https://ttp.cbp.dhs.gov/schedulerapi/slot-availability?locationId=5020"
SENDER_EMAIL = "weitianyi321@gmail.com"
APP_PASSWORD = "zrbu vdaq ovzw odsj"  # Use the app password generated
RECEIVER_EMAIL = "weitianyi321@gmail.com"
CHECK_INTERVAL = 3  # Check every 20 seconds
SEND_INTERVAL = 20

def create_email(subject, body, sender_email, receiver_email):
    """Create the email content."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg

def send_email(msg, sender_email, app_password, receiver_email):
    """Send the email using SMTP."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(sender_email, app_password)  # Login with email and app password
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_slot_availability(url):
    """Check the slot availability from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main():
    """Main function to check slot availability and send email if available."""
    while True:
        data = check_slot_availability(URL)
        if data and data.get("availableSlots"):
            subject = "Nexus appointment found"
            body = "Please check!" 
            email_msg = create_email(subject, body, SENDER_EMAIL, RECEIVER_EMAIL)
            send_email(email_msg, SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
