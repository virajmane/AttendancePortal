from flask import Flask, request, render_template, send_file
from tabulate import tabulate
import json
import string
import random
from replit import db
import os 
import csv

app = Flask(__name__)
@app.route("/<string:abbr>/", methods=["GET","POST"])
def index(abbr):
    if request.method=="GET":
        return render_template('index.html')

    else:
        fname = request.form["fname"]
        lname = request.form["lname"]
        roll = request.form["roll"]
        value = db[abbr]
        value.append([fname, lname, roll])
        db[abbr] = value
        return render_template('index2.html')

@app.route("/", methods=["GET","POST"])
def room():
    if request.method=="GET":
        return render_template('room.html')
    else:
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(5)))
        db[result_str] = []
        return render_template('room2.html', result_str = result_str)
        return f"Your attendence link is created: <a href = 'https://attend.virajman3.repl.co/{result_str}' target='_blank'>https://attend.virajman3.repl.co/{result_str}</a>"

@app.route("/<string:abbr>/show", methods=["GET","POST"])
def show(abbr):
    arr = []
    try:
        value = db[abbr]
    except:
        return render_template('error.html')
    for i in value:
        arr.append(i.value)
    #print(arr)
    return render_template('table.html', arr=arr, abbr = abbr)

@app.route('/<string:abbr>/download/', methods=['GET', 'POST'])
def download(abbr):
    value = db[abbr]
    value.insert(0, ["First Name", "Last Name", "Roll Number"])
    with open(f'/home/runner/attend/downloads/{abbr}.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(value)
    path = f"/home/runner/attend/downloads/{abbr}.csv"
    return send_file(path, as_attachment=True)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80, debug=True)