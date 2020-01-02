from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps # decorator'lar için

# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f) # tüm decorator'larda aynı
    def decorated_function(*args, **kwargs): # tüm decorator'larda aynı
        if "logged_in" in session: # session'ın içinde "logged_in" diye bir key value var mı?
            return f(*args, **kwargs) # tüm decorator'larda aynı // session başlamışsa normal bir şekilde çalıştırır
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","warning")
            return redirect(url_for("login")) # giriş yapmamışsa eğer, login ekranına yönlendiriyoruz 
    return decorated_function # tüm decorator'larda aynı

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

# Kullanıcı Login Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı: ")
    password = PasswordField("Parola: ")

# Makale Formu
class ArticleForm(Form):
    title = StringField("Makale Başlığı", validators=[
        validators.Length(min = 5, max = 100)])
    content = TextAreaField("Makale İçeriği", validators=[
        validators.Length(min = 10)])
    



app = Flask(__name__)  # flask'tan bir obje oluşturduk

app.secret_key = "ybblog" # kendimiz uydurabiliriz

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor" # aldığımız veriler sözlük yapısında gelir

# app ile mysql'i bağlamak istediğimiz için parametre olarak verdik. Flask ile MySql bağlantısını sağladık.
mysql = MySQL(app)


@app.route("/")  # (decorator)
def index():
    liste = [1, 2, 3, 4]  # demet'te olabilir ()
    return render_template("index3.html", numbers=liste)


@app.route("/about")
def about():
    return render_template("about.html")

# Kayıt Olma
@app.route("/register", methods = ["GET","POST"]) #hem get hem de post req alabilir
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate(): # submit butonuna basıldığında post req oluşur
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data) 
        # şifreleri encrypt ederek saklamak istiyoruz

        cursor = mysql.connection.cursor()
         # mySQL vt üzerinde işlem yapabilmemizi sağlayacak yapı: cursor

        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,email,username,password)) 
        # değerleri demet olarak veriyoruz
        # sorgu = "Insert into users(name,email,username,password) VALUES({},{},{},{})".format(name,email,username,password)

        mysql.connection.commit() # vt'da güncelleme yaptığımız için commit yapmalıyız.

        cursor.close()
        flash("Başarıyla kayıt oldunuz..","success")

        return redirect(url_for("login")) #index metoduyla ilişkili olan url adresine gider
    else:
        return render_template("register.html", form = form)

# Login İşlemi
@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm(request.form) # http request

    if request.method == "POST" and form.validate():
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "Select * From users where username = %s"

        result = cursor.execute(sorgu, (username, )) # (username, ) -> tek elemanlı demet syntax'i

        if result > 0:
            data = cursor.fetchone()
            real_password =data["password"] # tablodaki password alanını alıyoruz
            if sha256_crypt.verify(password_entered,real_password):
                # session
                session["logged_in"] = True
                session["username"] = username
                 
                flash("Başarıyla giriş yapıldı.","success")
                return redirect(url_for("index"))
            else:
                flash("Parola yanlış!","warning")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunamadı!","danger")
            return redirect(url_for("login"))

    return render_template("login.html", form = form)

# Logout işlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Kontrol Paneli
@app.route("/dashboard")
@login_required # dashboard çalıştırılmadan önce login_required'a gidecek
def dashboard():
    return render_template("dashboard.html")

# Makale Ekleme
@app.route("/addarticle", methods = ["POST", "GET"])
def addarticle():
    form = ArticleForm(request.form)
    return render_template("addarticle.html", form = form)


if __name__ == "__main__":
    app.run(debug=True)  # localhost'u çalıştır
