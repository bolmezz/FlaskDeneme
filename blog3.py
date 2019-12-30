from flask import Flask,render_template

app = Flask(__name__) #flask'tan bir obje oluşturduk


@app.route("/") # (decorator)
def index():
    liste = [1,2,3,4] # demet'te olabilir ()
    return render_template("index3.html",numbers = liste )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/article/<string:id>") # gelen id değerinin string old. söyledik
def detail(id):
    return "Article id : " + id

if __name__ == "__main__":
    app.run(debug=True) #localhost'u çalıştır

