from flask import Flask, render_template,request,redirect,url_for
from bson.objectid import ObjectId
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/contact_app"
db = PyMongo(app).db

@app.route('/')
def index():
    data = db.contacts.find()
    return render_template('index.html',data=data)



@app.route('/add_contact', methods=['POST','GET'])
def add_contact():  
    name = request.form['name']
    number = request.form['number']
    city = request.form['city']

    error=""
    print(name, number, city)
    print("***********************************************")

# Validation for Name
    
    if(isEmpty(name)):
        error = "Name is Empty"

    elif(isNotInRange(name , 3, 15)):
        error = "Name is either too short or too big"

    elif(not name.isalpha()):
        error = "Only Alphabets are allowed in Name"

# Validation for Number

    elif(isEmpty(number)):
        error = "Number is empty"
    elif(isNotInRange(number, 10, 10)):
        error = "Number must be a 10 digit number"

    elif(not number.isdigit()):
        error = "Only digits are allowed in Number"
    
# Validation for City

    elif(isEmpty(city)):
        error = "City name is Empty"

    elif(isNotInRange(city , 3, 15)):
        error = "City name is either too short or too big"

    elif(not city.isalpha()):
        error = "Only Alphabets are allowed in City"

    if(error != ""):
        return error, 401
    else:
        contact_data =  {
            "name": name,
            "number": number,
            "city": city

        }
        db.contacts.insert_one(contact_data)
        return url_for('index'), 200



@app.route('/delete', methods=['POST','GET'])
def delete():
    _id = request.form['_id']
    db.contacts.delete_one({"_id": ObjectId(_id)})
    return redirect(url_for("index"))




@app.route('/edit')
def edit():
    _id = request.args["_id"]
    data = db.contacts.find_one({"_id": ObjectId(_id)})
    return render_template("edit.html",data=data,id=_id)



@app.route('/edit_contact',methods=['POST','GET'])
def edit_contact():
    contact_data = {
        "name" : request.form["name"],
        "number": request.form["number"],
        "city": request.form["city"]
    }
    _id = request.form['_id']
    db.contacts.find_one_and_update({"_id":ObjectId(_id)}, {"$set": contact_data})
    return redirect(url_for('index'))

# Validation functions

def isEmpty(data):
    return True if (data == "" or data == " ") else False

def isNotInRange(data, minRange,maxRange):
    return False if (len(data) <= maxRange and len(data) >= minRange ) else True





if __name__ == '__main__':
    app.run(debug=True)