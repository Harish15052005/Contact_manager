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
    contact_data = {
        "name" : request.form["name"],
        "number": request.form["number"],
        "city": request.form["city"]
    }
    db.contacts.insert_one(contact_data)
    return redirect(url_for('index'))



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

if __name__ == '__main__':
    app.run(debug=True)