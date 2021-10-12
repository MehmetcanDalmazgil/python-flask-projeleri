from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__) # Uygulamayı çalıştır

# route = güzergah
@app.route("/") # Kaynak bu ise index metodunu çalıştır
def index():
    # return render_template("index.html", number = 10, number2 = 15) # Template'e yani şablonumuza yönlendirme gerçekleştirdik.
    #numbers = [1,2,3,4,5]
    #return render_template("index.html", numbers = numbers)
    return render_template("index.html")

@app.route("/search") # Kaynak bu ise search metodunu çalıştır
def search():
    return "Search Page"

@app.route("/toplam", methods = ["GET","POST"]) # toplam sayfasına get veya post işlemi yapılabilmektedir.
def toplam():
    if request.method == "POST": # Eğer bir post işlemi varsa yani index.html sayfası içerisinde bulunan form action edilmişse
        number1 = request.form.get("number1") # Form tarafından gelen istek içerisinden değerler alınmaktadır.
        number2 = request.form.get("number2")
        return render_template("number.html", total = int(number1) + int(number2)) # Toplamı ekranda bir şablon(template) ile gösterilir.
    else:
        #return render_template("number.html")
        return redirect(url_for("index")) # Bu şekilde sayfaya get request yapamamış oluyoruz. 

@app.route("/delete/item") # Kaynak bu ise delete metodunu çalıştır
def delete():
    return "Deleted item"

@app.route("/delete/<string:id>") # Dinamik url tanımlama 
def deleteId(id):
    return "Id: " + id 




if __name__ == "__main__":
    app.run(debug = True)

