import os,re,smtplib,ssl,datefinder,pytesseract
from PIL import Image
from email.message import EmailMessage
from datetime import datetime,date

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


def image_to_text(path_im):
    path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    image_path = path_im
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    ocr_text = text

    venue_pattern = r'\b(?:[A-Z][a-z]*\s)*[A-Z][a-z]*\s(?:[A-Z][a-z]*\s)*\b(?:Auditorium|Classroom|Hotel|Floor|Venue)\b'
    venues = re.findall(venue_pattern, ocr_text)
    if len(venues) > 0:
        venues = venues[0]
    else:
        venues = ''

    matches = datefinder.find_dates(ocr_text)
    ns = []
    for match in matches:
        s = str(match.date())
        if s[8:] in ocr_text:
            ns.append(s)
    if len(ns) > 0:
        dates = ns[-1]
    else:
        dates = ''

    time_pattern = r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b'
    times = re.findall(time_pattern, ocr_text)
    if len(times) > 0:
        # for i in times:
        times = convert(times[0]).rstrip()
        # print(times)
    else:
        times = ''

    return venues, dates, times


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
