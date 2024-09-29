import smtplib
import requests 
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv(".env\\.env")  # take environment variables

sender_email    = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_EMAIL_PWD')                                  #Set an app password on gmail
receiver_email  = os.getenv('RECEIVER_EMAIL')
url_to_check    = "http://mohibzahid.eastus.cloudapp.azure.com:8080/"           #Can set as an env.var as well


def send_email(subject, message):
  with smtplib.SMTP('smtp.gmail.com', 587) as server:           #Access Google domain and port
    server.starttls()                                           #Encryption enabled (Necessary)
    server.ehlo                                                 #A handshake to make server aware (Optional)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())

try:
  # Send a GET request to the health check URL
  response = requests.get(url_to_check)

  if response.status_code == 200:
    # Application is running
    message = MIMEText(f"Application is running! Response code: {response.status_code}")        #Email message
    message['Subject'] = "Application Status: Running"                                          #Email Subject
    send_email(message['Subject'], message)
  else:
    # Application is not running
    message = MIMEText(f"Application is not running! Response code: {response.status_code}")
    message['Subject'] = "Application Status: Not Running"
    send_email(message['Subject'], message)

except Exception as e:
  # Error occurred such as connection failure
  message = MIMEText(f"An error occurred: {str(e)}")
  message['Subject'] = "Application Status: Error"
  send_email(message['Subject'], message)
