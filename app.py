from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)



#Retrieve and Insert the Data 
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
       name = request.form['name']
       age = request.form['age']
       new_document = {"name":name,"age":age}
       mongo.db.inventory.insert_one(new_document) #Insert the Data in the Database

    documents = mongo.db.inventory.find() #Queries all the Data in the Database
    return render_template("index.html",documents=documents) 
@app.route('/about', methods=["GET", "POST"])
def about():
 

    
    return render_template("about.html") 


#Delete the Data 
@app.route('/delete/<string:_id>',methods=["GET", "POST"])
def delete_data(_id):
    document_id = ObjectId(_id)  # Convert the string _id to an ObjectId
    mongo.db.inventory.delete_one({"_id": document_id})
    return redirect(url_for('home'))

#Update the Data 
@app.route('/update_data/<string:_id>', methods=["GET", "POST"])
def update_data(_id):
    document_id = ObjectId(_id)  # Convert the string _id to an ObjectId
    document = mongo.db.inventory.find_one({"_id": document_id})  # Retrieve the existing document data

    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        filter_criteria = {"_id": document_id}
        update_data = {"$set": {"name": name, "age": age}}  
        # Changed the parameters
        mongo.db.inventory.update_one(filter_criteria, update_data)
        
        return redirect(url_for('home'))
    return render_template("update.html", document=document)




if __name__ =='__main__':
    app.run(debug=True)