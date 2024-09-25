import requests
import time
from urllib.parse import quote
import threading
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pygame

# Constants
URL = "https://ttp.cbp.dhs.gov/schedulerapi/slot-availability?locationId=5020"
SENDER_EMAIL = "weitianyi321@gmail.com"
APP_PASSWORD = "XXXXXX"  # Use the app password generated
RECEIVER_EMAIL = "weitianyi321@gmail.com"
CHECK_INTERVAL = 1  # Check every 1 seconds
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
    # try:
    #     server = smtplib.SMTP('smtp.gmail.com', 587)
    #     server.starttls()  # Enable security
    #     server.login(sender_email, app_password)  # Login with email and app password
    #     server.sendmail(sender_email, receiver_email, msg.as_string())
    #     server.quit()
    #     print("Email sent successfully!")
    #     time.sleep(SEND_INTERVAL)
    # except Exception as e:
    #     print(f"Failed to send email: {e}")

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

def play_sound():
    # Initialize the mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load("./media/chime-sound-7143.mp3")
    # Play the MP3 file
    pygame.mixer.music.play()
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def make_appointment(start_timestamp, end_timestamp):
    start_timestamp_encoded = quote(start_timestamp)
    end_timestamp_encoded = quote(end_timestamp)

    url = ("https://ttp.cbp.dhs.gov/scheduler?status=will-reschedule&reason=reschedule"
           "&zone=de00b6ee-c9a3-4420-b310-93de00562a64&appCode=GOES-126722058"
           "&appointmentId=42883602&appointmentStartTimestamp=" + start_timestamp_encoded +
           "&appointmentEndTimestamp=" + end_timestamp_encoded +
           "&locationId=5020&locationName=Blaine%20NEXUS%20And%20FAST%20Enrollment%20Center%20"
           "&tzData=America%2FLos_Angeles")

    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        print(response)
        return None


def main():
    """Main function to check slot availability and send email if available."""
    while True:
        data = check_slot_availability(URL)
        if data and data.get("availableSlots") \
                and '2024-09' in str(data.get("availableSlots")) \
                and '30' not in str(data.get("availableSlots")):
            # Create threads for each method
            slot = data['availableSlots'][0]  # Access the first available slot
            start_time = slot.get('startTimestamp')
            end_time = slot.get('endTimestamp')
            make_appointment(start_time, end_time)

            thread1 = threading.Thread(target=send_email)
            thread2 = threading.Thread(target=play_sound)

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait for both threads to complete
            thread1.join()
            thread2.join()

            subject = "Nexus appointment found"
            body = "Please check!"
            email_msg = create_email(subject, body, SENDER_EMAIL, RECEIVER_EMAIL)
            send_email(email_msg, SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL)
        print(datetime.now())
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
