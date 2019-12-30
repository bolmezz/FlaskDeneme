from flask import Flask,render_template

app = Flask(__name__) #flask'tan bir obje oluşturduk

@app.route("/") # (decorator)
def index():
    return render_template("index2.html")

if __name__ == "__main__":
    app.run(debug=True) #localhost'u çalıştır

