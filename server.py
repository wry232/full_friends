from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

@app.route('/', methods=["post", "get"])
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)

@app.route('/update', methods=["post"])
def update():
    idToUpdate = request.form["id"]
    query = "SELECT * FROM friends WHERE id = :specific_id"
    data = {'specific_id': idToUpdate}
    recordToUpdate = mysql.query_db(query, data)
    return render_template('update.html', recordToUpdate=recordToUpdate[0])

@app.route("/update_record", methods=["post"])
def update_record():
    updateData = {"first_name":request.form["first_name"], "last_name":request.form["last_name"], "email":request.form["email"], "id":request.form["id"]}
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
    mysql.query_db(query, updateData)
    return redirect("/")

@app.route('/add', methods=['post'])
def add():
    addUserData = {"first_name":request.form["first_name"], "last_name":request.form["last_name"], "email":request.form["email"]}
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    mysql.query_db(query, addUserData)
    return redirect('/')

@app.route('/delete', methods=["post"])
def delete():
    deleteUser = {"id":request.form["id"]}
    query = "DELETE FROM friends WHERE id = :id"
    mysql.query_db(query, deleteUser)
    return redirect("/")

@app.route("/deleteConfirmation", methods=["post"])
def deleteConfirmation():
    idToDelete = request.form["id"]
    return render_template("confirm_delete.html", idToDelete=idToDelete)

app.run(debug=True)
