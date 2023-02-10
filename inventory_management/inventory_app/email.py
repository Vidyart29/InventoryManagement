import smtplib
from email.message import EmailMessage

def sendMail(emailAddress, Content):
    fromEmail = 'jensleework@gmail.com'
    msg = EmailMessage()
    msg["Subject"] = "Recent Order"
    msg["From"] = fromEmail
    msg["TO"] = emailAddress
    msg.set_content(Content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(fromEmail, "")
        print("Sending mail to ", )
        smtp.send_message(msg)  
