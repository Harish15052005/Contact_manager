from flask import Flask, render_template,request,redirect,url_for,flash
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import forms

app = Flask(__name__)
app.config["SECRET_KEY"] = "Your Secret Key"
app.config["MONGO_URI"] = "your mongoDB URI"
db = PyMongo(app).db

@app.route('/', methods=['POST','GET'])
def index():
    form = forms.ContactForm()
    data = db.contacts.find()
    if form.validate_on_submit():
        
        if(db.contacts.find_one({'name': form.name.data})):
            form.name.errors.append("Name already present")
            return render_template('index.html', data=data, form=form)

        if(db.contacts.find_one({'number': form.number.data})):
            form.number.errors.append("Number already present")
            return render_template('index.html', data=data, form=form)
            
        contact_data =  {
            "name": form.name.data,
            "number": form.number.data,
            "city": form.city.data
        }
        db.contacts.insert_one(contact_data)
        return redirect(url_for("index"))
    return render_template('index.html',data=data, form=form)


@app.route('/delete', methods=['POST','GET'])
def delete():
    _id = request.form['_id']
    db.contacts.delete_one({"_id": ObjectId(_id)})
    return redirect(url_for("index"))

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    form = forms.ContactForm()
    try:
        name = request.args["name"]
        data = db.contacts.find_one({"name": name})
    except:
        return "<h1> Error !! </h1>",500
    if form.validate_on_submit():
        if(form.name.data == data['name'] and form.number.data == data['number'] and form.city.data == data['city']):
            form.city.errors.append("No data has been changed")
            return render_template("edit.html", data=data, form=form)

        if(form.name.data != data['name']):
            if(db.contacts.find_one({"name" : form.name.data})):
                form.name.errors.append("Name already present!!")
                return render_template("edit.html", data=data, form=form)

        if(form.number.data != data['number']):
            if(db.contacts.find_one({"number": form.number.data})):
                form.number.errors.append("Number Already Present!!")
                return render_template("edit.html", data=data, form=form)
        
        NewData = {
            "name" : form.name.data,
            "number" : form.number.data,
            "city" : form.city.data
        }
        print(NewData)
        db.contacts.find_one_and_update({"name": name}, {"$set" : NewData})
        return redirect(url_for("index"))
    
    return render_template("edit.html" , data=data, form=form)

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template("about.html")
if __name__ == '__main__':
    app.run(debug=True)