from flask import Flask,render_template

app = Flask(__name__) #flask'tan bir obje oluşturduk

# __name__ -> özel bir değişken. Dosyayı direkt terminalden çalıştırırsak bu değişkenin adı __main__ olur.
# python dosyasını başka bir dosyadan açarsak __name__'in adı başka olur.

@app.route("/") # (decorator) bir response dönmek istiyorum. requesti root olarak yapıyoruz.bu req yapınca metod direkt çalışacak.
def index():
    sayi = 10
    sayi2 = 20

    article = dict()
    article["title"] = "Deneme"
    article["body"] = "Deneme 123"
    article["author"] = "Beyza Ölmez" #key-value değerleri

    return render_template("index.html",number = sayi,number2 = sayi2,article = article) # html dosyasını render edip dönecek
    #jinja templ özelliği (html dosyası için) : burada bir python verisi kullanacaksak {{ }} içinde kullan. Bunlar python kodu olarak yorumlanır.

@app.route("/about") #localhost:5000/about
def about():
    return "Hakkımda"  #response. Açılan sayfada görünecek string.

if __name__ == "__main__":
    app.run(debug=True) #localhost'u çalıştır

