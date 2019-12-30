from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

# Kullanıcı Kayıt Formu


class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(
        min=4, max=25)])  # StringField class'ından türettik
    username = StringField("Kullanıcı Adı", validators=[
                           validators.Length(min=5, max=35)])
    email = StringField("Email Adresi", validators=[
                        validators.Email(message="Geçerli mail adresi girin.")])
    password = PasswordField("Parola", validators=[validators.DataRequired(
        message="Lütfen bir parola belirleyin."), validators.EqualTo(fieldname="confirm", message="Parola uyuşmuyor.")])
    confirm = PasswordField("Parolayı Tekrar Girin")


app = Flask(__name__)  # flask'tan bir obje oluşturduk

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYQGL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# app ile mysql'i bağlamak istediğimiz için parametre olarak verdik. Flask ile MySql bağlantısını sağladık.
mysql = MySQL(app)


@app.route("/")  # (decorator)
def index():
    liste = [1, 2, 3, 4]  # demet'te olabilir ()
    return render_template("index3.html", numbers=liste)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)  # localhost'u çalıştır
