from flask import Flask,render_template,request,redirect,flash,url_for, make_response  
from pymongo import MongoClient

from gridfs import GridFS  


import matplotlib.pyplot as plt

import pymongo as mongo
app = Flask(__name__)
app.config['SECRET_KEY']="oohlala"
url=f'mongodb+srv://trailUsername:trialPassword@trailcluster.dhfoi.mongodb.net/test'
client = mongo.MongoClient(url)
db = client["avalanche"]
grid_fs = GridFS(db)
events_db=db["events"]
users_db=db.users

# events_db.insert_one(
#                 {
#                     "poster": 'static/images/brochure.jpeg',
#                     "name": 'test4',
#                     "datetime": '28/03/2023 13:00',
#                     "venue": 'lecture hall 233'
#                 }
#             )

# users_db.insert_one(
#                 {
#                     "email": 'walala@gmail.com',
#                     "password": 'test4',
                    
#                 }
#             )

@app.route('/',methods=['GET','POST'])
def events():
   
    event=events_db.find()
    return render_template('events.html',event=event)

# @app.route('/addevent')
# def addevent():
#     return render_template('addevent.html')

@app.route('/userlogin',methods=["GET","POST"])
def userlogin():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user=users_db.find_one(
            {'email':email}
            )
        if user !=None :
            if user['password']==password:
                var=True
                event=events_db.find()
                return render_template('events.html',event=event,var=var)
            else:
                var=False
                flash("Incorrect Password")
        else:
            var=False
            flash("user doesnt Exist")
        
       

        # return render_template('userlogin.html',email=email,password=password)
  
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
                users_db.insert_one(
                        {
                            "email": email,
                            "password": password,
                            
                        }
                    )
                return render_template('userlogin.html')
            else:
                flash('passwords donot match')
        else:
            flash('Mail-id already exists')
    return render_template('userregister.html')


@app.route('/categories')
def categories():
    return render_template('categories.html')


if __name__ == '__main__':
    app.run(debug=True)