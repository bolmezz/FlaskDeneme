from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt


app = Flask(__name__) #flask'tan bir obje oluşturduk

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYQGL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app) # app ile mysql'i bağlamak istediğimiz için parametre olarak verdik. Flask ile MySql bağlantısını sağladık.


@app.route("/") # (decorator)
def index():
    liste = [1,2,3,4] # demet'te olabilir ()
    return render_template("index3.html",numbers = liste )

@app.route("/about")
def about():
    return render_template("about.html")
