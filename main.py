from flask import Flask, request, render_template, redirect, url_for, session
from os import path
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "secretkey"

pic = path.join('static', 'photos')
app.config["UPLOAD_FOLDER"] = pic

ROOT = path.dirname(path.relpath(__file__))

connect = sql.connect(path.join(ROOT, 'users.db'), check_same_thread=False)
curser = connect.cursor()

cnnt = sql.connect(path.join(ROOT, 'products.db'), check_same_thread=False)
crsr = cnnt.cursor()

# products.db IS A DATABASE WHERE TABLE products CONTAINS PRODUCT DETAILS

# cursr = cnnt.cursor()
# cursr.execute("""CREATE TABLE products(
#         id int PRIMARY KEY,
#         products VARCHAR(20) NOT NULL,
#         price int NOT NULL,
#         description VARCHAR(100) NOT NULL
# )""")
# cnnt.commit()
# cnnt.close()

@app.route("/")
def homepage():
    pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
    pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
    pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
    pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
    return render_template("home.html", pic=pic, pic1=pic1, pic2=pic2, pic3=pic3)

@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
        pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
        pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
        pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
        username = request.form['username1']
        session['username'] = username
        password = request.form['password1']
        rid = curser.execute("SELECT rowid FROM users").fetchall()
        usrnme = curser.execute("SELECT username FROM users").fetchall()
        pas = curser.execute("SELECT password FROM users WHERE username= (?)", (username,)).fetchall()
        for i in range(len(rid)):
            final_name = ''.join(usrnme[i])
            if username == final_name:
                final_pass = ''.join(pas[0])
                if password == final_pass:
                    return redirect(url_for('my_homepage'))
                else:
                    return render_template("login.html", info ="Invalid password")
            else:
                i += 1
        if request.method == 'GET':
            pass
    return render_template("login.html")

@app.route("/signup", methods=['POST','GET'])
def signup():
    pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
    pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
    pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
    pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        session["email"] = email
        phone = request.form['phno']
        address = request.form['address']
        curser.execute("INSERT INTO users (username, password, email, phone, address) VALUES (?, ?, ?, ?, ?)",
                   (username, password, email, phone, address))
        connect.commit()

# NEW TABLE IS CREATED AUTOMATICALLY NAMED AFTER THE USER'S USERNAME, WHICH STORES INFORMATION ABOUT THE USER'S CART

        crsr.execute("""CREATE TABLE {}(
                cart VARCHAR(20) NOT NULL, constraint fk_cart
                foreign key(cart)
                references products(products)
        )""".format(username))
        cnnt.commit()
        cnnt.close()
        return redirect(url_for('myhomepage'))
    return render_template("signup.html")

@app.route("/my-homepage")
def myhomepage():
    if 'email' in session:
        email = session['email']
        name = curser.execute("SELECT username FROM users WHERE email= (?)", (email,)).fetchall()
        final_name = ''.join(name[0])
        pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
        pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
        pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
        pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
        return render_template("users_homepage.html", pic=pic, pic1=pic1, pic2=pic2, pic3=pic3, name1= final_name)
    else:
        pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
        pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
        pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
        pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
        return render_template("users_homepage.html", pic=pic, pic1=pic1, pic2=pic2, pic3=pic3)

@app.route("/my_homepage")
def my_homepage():
    if 'username' in session:
        username = session['username']
        pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
        pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
        pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
        pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
        return render_template("users_homepage.html", pic=pic, pic1=pic1, pic2=pic2, pic3=pic3, name=username)
    else:
        pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
        pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
        pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
        pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
        return render_template("users_homepage.html", pic=pic, pic1=pic1, pic2=pic2, pic3=pic3)

@app.route("/my_cart")
def my_cart():
    username = session['username']
    cart = crsr.execute("SELECT products.products, products.description, products.price FROM {} INNER JOIN products".format(username)).fetchall()
    return render_template("my_cart.html", cart= cart)


if __name__ == "__main__":
    app.run(debug=True)