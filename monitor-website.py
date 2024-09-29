import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv(".env\\.env")  # take environment variables

email_address  = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')
msg            = "Subject: SITE DOWN\nFix the issue"


response = requests.get('http://mohibzahid.eastus.cloudapp.azure.com:8080/')

if False:
    print("Application is running successfully")
else:
    print("Application down. Fix it")

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            smtp.ehlo()
            smtp.login("e-21f-bscs-44@students.duet.edu.pk", "Balistic6261")
            smtp.sendmail("e-21f-bscs-44@students.duet.edu.pk", "mohibzahid97@gmail.com", msg)
            print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to log in. Please check your email credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")