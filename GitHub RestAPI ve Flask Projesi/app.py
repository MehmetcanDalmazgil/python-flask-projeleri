# Kaynak : https://github.com/mustafamuratcoskun/Github-Api-Flask-Python

from flask import Flask,render_template,request
import requests
app = Flask(__name__)
base_url = "https://api.github.com/users/"

@app.route("/",methods = ["GET","POST"]) # Bu sayfa üzerinden get ve post işlemi yapılabileceğini belirtiyoruz.
def index():
    if request.method == "POST": # Eğer bir post olduysa
        githubname = request.form.get("githubname") # Kullanıcı tarafından girilen ismi alıyoruz.
        response_user = requests.get(base_url + githubname) # Adresi get ile sorguluyoruz. 
        response_repos = requests.get(base_url + githubname + "/repos") # Adreis get ile sorguluyoruz.

        # Dönen değerleri json formatına çeviriyoruz.
        user_info = response_user.json() 
        repos = response_repos.json()
        
        if "message" in user_info: # Eğer içerisinde mesaj adlı bir değişken varsa
            return render_template("index.html",error = "Kullanıcı Bulunamadı...")
        else:

            return render_template("index.html",profile = user_info,repos = repos)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)