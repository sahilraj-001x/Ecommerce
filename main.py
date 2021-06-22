from flask import Flask, request, render_template, redirect, url_for, session, flash
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


# id = input('id :')
# products = input('products :')
# price = input('price :')
# description = input('description :')
# cursr = cnnt.cursor()
# cursr.execute("INSERT INTO products (id, products, price, description) VALUES(?, ?, ?, ?)", (id, products, price, description,))
# cnnt.commit()
# cnnt.close()

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
                references products(products),
        )""".format(username))
        cnnt.commit()
        cnnt.close()
        return redirect(url_for('my_homepage'))
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
        return render_template("home.html", pic=pic, pic1=pic1, pic2=pic2, pic3=pic3, name= final_name)
    else:
        pic = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
        pic1 = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
        pic2 = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
        pic3 = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
        return render_template("home.html", pic=pic, pic1=pic1, pic2=pic2, pic3=pic3)

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

@app.route("/my_cart", methods= ['POST', 'GET'])
def my_cart():
    username = session['username']
    cart = crsr.execute("SELECT products.products, products.description FROM {} INNER JOIN products ON products.products= {}.cart".format(username, username)).fetchall()
    amount = crsr.execute("SELECT products.price FROM {} INNER JOIN products ON products.products= {}.cart".format(username, username)).fetchall()
    if request.method == 'POST':
        return redirect(url_for('address'))
    return render_template("my_cart.html",name= username, cart= cart, amount= amount)

@app.route("/address", methods= ['POST', 'GET'])
def address():
    address = request.form.get('address')
    username = session['username']
    curser.execute("UPDATE users SET address= (?) WHERE username = (?)", (address,) + (username,))
    connect.commit()
    if request.method == 'POST':
        return redirect(url_for('order_details'))
    return render_template('address.html')

@app.route("/order-details")
def order_details():
    username = session['username']
    cart = crsr.execute("SELECT products.products, products.description FROM {} INNER JOIN products ON products.products= {}.cart".format(username, username)).fetchall()
    amount = crsr.execute("SELECT products.price FROM {} INNER JOIN products ON products.products= {}.cart".format(username,username)).fetchall()
    return render_template("buy.html", name=username, cart=cart, amount=amount)

@app.route("/product-macbook-pro", methods = ['POST', 'GET'])
def macbook():
    mac = path.join(app.config["UPLOAD_FOLDER"], "mac.png")
    username = session['username']
    if request.method == 'POST':
        crsr.execute("INSERT INTO {} VALUES ('MacBook')".format(username))
        cnnt.commit()
        return redirect(url_for('my_homepage'))
    return render_template("macbook.html", pic= mac)

@app.route("/product-hp", methods = ['POST', 'GET'])
def hp():
    mac = path.join(app.config["UPLOAD_FOLDER"], "hp.png")
    username = session['username']
    if request.method == 'POST':
        crsr.execute("INSERT INTO {}(cart) VALUES ('HP')".format(username))
        cnnt.commit()
        return redirect(url_for('my_homepage'))
    return render_template("hp.html", pic= mac)

@app.route("/product-dell", methods = ['POST', 'GET'])
def dell():
    mac = path.join(app.config["UPLOAD_FOLDER"], "dell.png")
    username = session['username']
    if request.method == 'POST':
        crsr.execute("INSERT INTO {} VALUES ('Dell')".format(username))
        cnnt.commit()
        return redirect(url_for('my_homepage'))
    return render_template("dell.html", pic= mac)

@app.route("/product-asus", methods = ['POST', 'GET'])
def asus():
    mac = path.join(app.config["UPLOAD_FOLDER"], "asus.png")
    username = session['username']
    if request.method == 'POST':
        crsr.execute("INSERT INTO {} VALUES ('ASUS')".format(username))
        cnnt.commit()
        return redirect(url_for('my_homepage'))
    return render_template("asus.html", pic= mac)

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)
