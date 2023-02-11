import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())


def sendMail(emailAddress, Content):
    fromEmail = os.getenv("GMAIL_APP_EMAIL")
    fromPassword = os.getenv("GMAIL_APP_SECRET_PASSWORD")
    print(fromEmail)
    msg = EmailMessage()
    msg["Subject"] = "Recent Order"
    msg["From"] = fromEmail
    msg["TO"] = emailAddress
    msg.set_content(Content)
    print("message settt")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(fromEmail, fromPassword)
            print("Sending mail to ", emailAddress)
            smtp.send_message(msg)
            print("Sent mail")
    except Exception as e:
        print("Email not sent; Error : ", e)
