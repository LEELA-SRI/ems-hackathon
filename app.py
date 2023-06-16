from flask import Flask, render_template, request, flash, session, redirect, url_for
from hashlib import sha256
import pymongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from PIL import Image
from pytesseract import pytesseract
import re
import os
from datetime import date
import datefinder


app = Flask(__name__)

app.config['SECRET_KEY'] = "oohlala"
app.config['UPLOAD_FOLDER'] = 'static/images/uploaded'
uri = f"mongodb+srv://trailUsername:trialPassword@trailcluster.dhfoi.mongodb.net/test"


client = pymongo.MongoClient(uri)


db = client.avalanche


events_db = db.events
users_db = db.users
brochures_db = db.brochures


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


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def events():

    if session.items() and session['email']:
        var = True
    else:
        var = False
    today_date = str(date.today())
    event = events_db.find()
    return render_template('events.html', event=event, var=var, today_date=today_date)


@app.route('/userlogin', methods=["GET", "POST"])
def userlogin():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = users_db.find_one(
            {'email': email}
        )
        if user:
            if sha256(str(password).encode()).hexdigest() == user['password']:
                session['email'] = email

                return redirect(url_for('addevent'))
            else:
                flash("Incorrect Password")
        else:
            flash("user doesnt Exist")
    return render_template('userlogin.html')


@app.route('/registerUser', methods=['GET', 'POST'])
def userregister():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        user = users_db.find_one(
            {'email': email}
        )
        if user == None:
            if password == cpassword:
                hashpass = sha256(str(password).encode()).hexdigest()
                users_db.insert_one({'email': email, 'password': hashpass})
                session['email'] = email
                return render_template('userlogin.html')
            else:
                flash('passwords donot match')
        else:
            flash('Mail-id already exists')
    return render_template('userregister.html')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect('/home')
    else:
        return redirect('/home')


@app.route("/addevent", methods=["POST", "GET"])
def addevent():
    if session.items() and session['email']:

        if request.method == 'POST':
            if 'uploaded_file' not in request.files:
                flash("No file is uploaded")
            brochure = request.files['uploaded_file']
            if brochure.filename == '':
                flash("No img selected")
            if brochure and allowed_file(brochure.filename):
                brochure.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), app.config['UPLOAD_FOLDER'], secure_filename(brochure.filename)))
                brochures_db.insert_one(
                    {
                        'uploaded_brochure': f'static/images/uploaded/{secure_filename(brochure.filename)}'
                    }
                )
                venue_event = image_to_text(
                    f'static/images/uploaded/{secure_filename(brochure.filename)}')[0]
                date_event = image_to_text(
                    f'static/images/uploaded/{secure_filename(brochure.filename)}')[1]
                time_event = image_to_text(
                    f'static/images/uploaded/{secure_filename(brochure.filename)}')[2]
                show = True
                return render_template('addevent.html', poster=f'static/images/uploaded/{secure_filename(brochure.filename)}', venue=venue_event, date=date_event, time=time_event, show=show)

        return render_template('addevent.html')
    else:
        return redirect('/userlogin')


@app.route('/upload', methods=["POST"])
def upload():
    event_name = request.form.get('event_name')
    event_date = request.form.get('event_date')
    event_time = request.form.get('event_time')
    event_venue = request.form.get('event_venue')
    event_eligibility = request.form.get('event_eligibility')
    event_awards = request.form.get('event_awards')
    event_desc = request.form.get('event_desc')
    event_deadline = request.form.get('event_deadline')
    event_limit = request.form.get('event_limit')
    dept = request.form.get('dept')
    print(dept)
    event_cord = request.form.get('event_cord')
    broc = brochures_db.find().sort('_id', pymongo.DESCENDING).limit(1)
    for i in broc:
        file_path = i['uploaded_brochure']
    events_db.insert_one(
        {
            'poster': file_path,
            'name': event_name,
            'venue': event_venue,
            'date': event_date,
            'time': event_time,
            'awards': event_awards,
            'eligibility': event_eligibility,
            'desc': event_desc,
            'deadline': event_deadline,
            'rlimit': event_limit,
            'dept': dept,
            'contact': event_cord


        }
    )
    flash('Event added successfully!')

    return redirect('/home')


@app.route('/<id>/edit', methods=['GET', 'POST'])
def edit_event(id):
    event = events_db.find_one({"_id": ObjectId(id)})
    return render_template('modify.html', id=id, event=event)


@app.route('/update_event/<id>', methods=['GET', 'POST'])
def update_event(id):
    event_name = request.form.get('event_name')
    event_date = request.form.get('event_date')
    event_time = request.form.get('event_time')
    event_venue = request.form.get('event_venue')
    event_eligibility = request.form.get('event_eligibility')
    event_awards = request.form.get('event_awards')
    event_desc = request.form.get('event_desc')
    event_deadline = request.form.get('event_deadline')
    event_limit = request.form.get('event_limit')
    dept = request.form.get('dept')
    event_cord = request.form.get('event_cord')
    event = events_db.update_one({"_id": ObjectId(id)},
                                 {"$set": {
                                     'name': event_name,
                                     'venue': event_venue,
                                     'date': event_date,
                                     'time': event_time,
                                     'awards': event_awards,
                                     'eligibility': event_eligibility,
                                     'desc': event_desc,
                                     'deadline': event_deadline,
                                     'rlimit': event_limit,
                                     'dept': dept,
                                     'contact': event_cord
                                 }}
                                 )
    print(events_db.find_one({"_id": ObjectId(id)}))
    flash('Event updated successfully!')
    return redirect('/home')


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    print(id)
    events_db.delete_one({"_id": ObjectId(id)})
    flash('Event Deleted successfully!')

    return redirect('/home')


@app.route('/<event_name>/register', methods=['GET', 'POST'])
def event_register(event_name=None):
    return render_template('base.html', event_name=event_name)


@app.route('/categories')
def categories():
    department = request.args.get('department')
    event_name = request.args.get('name')
    month = request.args.get('month')
    filters = {}
    if department:
        filters['dept'] = department
    if event_name:
        filters['name'] = {'$regex': event_name, '$options': 'i'}
    if month:
        filters['date'] = {'$regex': f'{month}-'}
    filtered_events = list(events_db.find(filters))

    return render_template('categories.html', filtered_events=filtered_events)


if __name__ == '__main__':
    app.run(debug=True)
