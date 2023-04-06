from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_pymongo import PyMongo
from hashlib import sha256
# from gridfs import GridFS  
import pymongo 
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

app.config['SECRET_KEY']="oohlala"
app.config['UPLOAD_FOLDER']='static/images/uploaded'
uri=f"mongodb+srv://trailUsername:trialPassword@trailcluster.dhfoi.mongodb.net/test"
# mongo = PyMongo(app)
client = pymongo.MongoClient(uri)
db=client.avalanche

# db=mongo.avalanche

# grid_fs = GridFS(db)

events_db=db.events
users_db=db.users
brochures_db=db.brochures

ALLOWED_EXTS=set(['png','jpg','jpeg','webp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTS


# events_db.insert_one(
#                 {
#                     "poster": 'static/images/brochure.jpeg',
#                     "name": 'test5',
#                     "datetime": '28/03/2023 13:00',
#                     "venue": 'lecture hall 233'
#                 }
#             )


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
            # save_brochure=secure_filename(brochure.filename)
            brochure.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(brochure.filename)))
            brochures_db.insert_one(
                {
                'uploaded_brochure': f'static/images/uploaded/{secure_filename(brochure.filename)}'
                }
            )
            events_db.insert_one(
                {
                'poster': f'static/images/uploaded/{secure_filename(brochure.filename)}'
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