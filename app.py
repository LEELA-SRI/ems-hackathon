from flask import Flask,render_template,request,flash,session,redirect,url_for
from hashlib import sha256
import pymongo 
from werkzeug.utils import secure_filename
from PIL import Image
from pytesseract import pytesseract
import re
import os


app = Flask(__name__)

app.config['SECRET_KEY']="oohlala"
app.config['UPLOAD_FOLDER']='static/images/uploaded'
uri=f"mongodb+srv://trailUsername:trialPassword@trailcluster.dhfoi.mongodb.net/test"


client = pymongo.MongoClient(uri)


db=client.avalanche


events_db=db.events
users_db=db.users
brochures_db=db.brochures

ALLOWED_EXTS=set(['png','jpg','jpeg','webp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTS

def image_to_text(path_im):
    path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    image_path = path_im
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(image_path )
    text = pytesseract.image_to_string(img)
    ocr_text=text.lower().capitalize()
    venue_pattern = r'\b(?:[A-Z][a-z]*\s)*[A-Z][a-z]*\s(?:[A-Z][a-z]*\s)*\b(?:Auditorium|Classroom|Hotel|Floor|Venue)\b'
    venues = re.findall(venue_pattern, ocr_text)

    date_pattern = r"(\d{1,2})\s(January|February|March|April|May|June|July|August|September|October|November|December|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d{4})"
    dates = re.findall(date_pattern, ocr_text)

    time_pattern = r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b'
    times = re.findall(time_pattern, ocr_text)

    return venues,dates,times


@app.route('/home',methods=['GET','POST'])
def events():
    print(bool(session.items()))
    if session.items() and session['email']:
        var=True
    else:
        var=False
    if request.method=='POST':
        if 'uploaded_file' not in request.files:
            flash("No file is uploaded")
        brochure=request.files['uploaded_file']
        if brochure.filename=='':
            flash("No img selected")
        if brochure and allowed_file(brochure.filename):
            brochure.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(brochure.filename)))
            brochures_db.insert_one(
                {
                'uploaded_brochure': f'static/images/uploaded/{secure_filename(brochure.filename)}'
                }
            )
            venue_event=image_to_text(f'static/images/uploaded/{secure_filename(brochure.filename)}')[0]
            date_event=image_to_text(f'static/images/uploaded/{secure_filename(brochure.filename)}')[1]
            time_event=image_to_text(f'static/images/uploaded/{secure_filename(brochure.filename)}')[2]
            events_db.insert_one(
                {
                'poster': f'static/images/uploaded/{secure_filename(brochure.filename)}',
                'name':'some new event',
                'venue':venue_event,
                'date': date_event ,
                'time':time_event
                }
            )

    event=events_db.find()
    return render_template('events.html',event=event,var=var)


@app.route('/userlogin',methods=["GET","POST"])
def userlogin():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user=users_db.find_one(
            {'email':email}
            )
        if user:
            if sha256(str(password).encode()).hexdigest()==user['password']:
                session['email'] = email
                event=db.events.find()
                return redirect(url_for('events'))
            else:
                flash("Incorrect Password")
        else:
            flash("user doesnt Exist")
    return render_template('userlogin.html')


@app.route('/registerUser',methods=['GET','POST'])
def userregister():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        user=users_db.find_one(
                {'email':email}
                )
        if user==None:
            if password==cpassword:
                hashpass = sha256(str(password).encode()).hexdigest()
                users_db.insert_one({'email' : email, 'password' : hashpass})
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
    
@app.route('/categories')
def categories():
    return render_template('categories.html')


if __name__ == '__main__':
    app.run(debug=True)