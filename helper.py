import os,re,smtplib,ssl,datefinder,pytesseract
from PIL import Image
from email.message import EmailMessage
from datetime import datetime

ALLOWED_EXTS = set(['png', 'jpg', 'jpeg', 'webp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS


def convert(string):

    if string[-2:] == "AM" and string[:2] == "12":
        return "00" + string[2:-2]

    elif string[-2:] == "AM":
        return string[:-2]

    elif string[-2:] == "PM" and string[:2] == "12":
        return string[:-2]

    else:
        return str((string[:2]) + '12') + string[2:8]




def send_email_notification(data, event):
    sender_email = os.environ['SENDER_MAIL_ID']
    password = os.environ['SENDER_APP_KEY']
    receiver_email = data['email']
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = data['email']
    em["subject"] = "Registration success"
    message = f"Hey {data['name']},\n\nYou have successfully registered for {data['event_name']}.Make sure to be there on {event['date']} at {event['venue']}\n\nBest of luck!\nFor further queries contact {event['contact']}."
    em.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())


def date_validator(date1, date2):
    try:
        dt1 = datetime.strptime(date1, "%Y-%m-%d")
        dt2 = datetime.strptime(date2, "%Y-%m-%d")
        if dt1 >= dt2:
            return True
        else:
            return False
    except ValueError:
        return False
