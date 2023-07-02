import os,re,smtplib,ssl,datefinder,pytesseract
from flask import flash
from PIL import Image
from email.message import EmailMessage
import urllib.parse
import datetime
from datetime import timedelta


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


import urllib.parse

def generate_google_calendar_link(event):
    event_title = event['name']
    event_date = event['date']
    event_time = event['time']
    event_location = event['venue']
    event_datetime = datetime.datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
    event_datetime=event_datetime.astimezone(datetime.UTC)
    start_datetime = event_datetime.strftime("%Y%m%dT%H%M%SZ")
    end_datetime = (event_datetime + timedelta(hours=1)).strftime("%Y%m%dT%H%M%SZ")

    encoded_event_title = urllib.parse.quote(event_title)
    encoded_event_location = urllib.parse.quote(event_location)

    calendar_link = f"https://www.google.com/calendar/render?action=TEMPLATE&text={encoded_event_title}&dates={start_datetime}/{end_datetime}&location={encoded_event_location}"

    return calendar_link



def send_email_notification(data, event):
    print(data,event)
    sender_email = os.environ['SENDER_MAIL_ID']
    password = os.environ['SENDER_APP_KEY']
    receiver_email = data['email']
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = data['email']
    

    em["subject"] = "Registration success"
    message = f"Hey {data['name']},\n\nYou have successfully registered for {data['event_name']}.Make sure to be there on {event['date']} at {event['venue']}\n\nBest of luck!\n"
    message+=f"{'For further queries contact'+ event['contact'] if   event['contact'] else ''}"
    event_link = generate_google_calendar_link(event)
    message += f"\n\nAdd this event to your Google Calendar: {event_link}"

    em.set_content(message)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls(context=context)
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, receiver_email, em.as_string())
        flash("Email sent successfully!")
    except (smtplib.SMTPException, smtplib.SMTPServerDisconnected) as e:
        flash(f"An error occurred while sending the email: {str(e)}")


def date_validator(date1, date2):
    try:
        dt1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
        dt2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        if dt1 >= dt2:
            return True
        else:
            return False
    except ValueError:
        return False
