from io import BytesIO
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from .models import Friend, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

auth = Blueprint('auth', __name__)

code = 0

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if user.password == password:
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password', category='error')

    return render_template("/login/login.html", boolean=True)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email = email, first_name = first_name, password = password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('Account created!', category = 'success')
            return redirect(url_for('views.home'))

    return render_template("login/signup.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    friends = Friend.query.order_by(Friend.id)
    return render_template('dashboard.html', friends = friends)

@auth.route('/explore')
@login_required
def explore():
    our_users = User.query.order_by(User.id)
    id = current_user.id
    return render_template('explore.html', our_users = our_users)

@auth.route('/users')
@login_required
def users():
    id = current_user.id
    our_users = User.query.order_by(User.id)
    if id == 1:
        return render_template('users.html', our_users = our_users)
    else:
        return render_template('explore.html', our_users = our_users)

@auth.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        user = current_user

        npass = request.form.get('newPassword')
        picture = request.files['picture'].read()

        if len(npass) > 0:
            user.password = npass
            print(len(user.password))
            if len(user.password) < 8:
                flash('Password must be at least 8 characters.', category='error')
            else:
                db.session.add(user)
                db.session.commit()
        if picture != None:
            user.pictureData = picture
            db.session.add(user)
            db.session.commit()

    return render_template('settings.html')

@auth.route('/delete')
@login_required
def delete():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit() 
    flash("Account deleted")
    return redirect(url_for('auth.login'))

@auth.route('/deleteUser/<id>', methods=['GET', 'POST'])
@login_required
def deleteUser(id):
    your_id = current_user.id
    if your_id == 1:
        userid = id
        User.query.filter_by(id=userid).delete()
        db.session.commit()
        flash("Account deleted")
    return redirect("/users")

@auth.route('/recover', methods=['GET', 'POST'])
def recover():
    numbers = 0
    i = 10

    for num in range(6):
        numbers += (random.randint(0,9)) * i
        i = i * 10

    numbers = int(numbers / 10)

    if request.method == 'POST':
        form_name = request.form['form-name']

        if form_name == 'form1':
            email = request.form.get('email')
            user = User.query.filter_by(email = email).first()


            sender_email = "yemima.root@gmail.com"
            receiver_email = email
            password = "qabr ezcs sgix amug"

            #Create MIMEMultipart object
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Recover Password"
            msg["From"] = sender_email
            msg["To"] = receiver_email

            #HTML Message Part
            html = """\
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
                    <style>                        
                        body {
                            font-family: 'Montserrat', sans-serif;                            background-color: #F1F1F1;
                            color: #303030;
                        }

                        img {
                            margin: auto;
                            text-align: center;
                        }

                        div {
                            margin: auto;
                            text-align: center;
                            border-radius: 10px;
                            background-color: #ffffff;
                            width: 50%;
                            border-style: solid;
                            border-color: #E6E6E6;
                            border-width: 1px;
                        }

                        a {
                            text-decoration: none;
                        }

                    </style>
                </head>
                <body>
                    <h2 style="text-align: center;">Password Recovery</h2>
                    <br>
                    <div>
                        <h1>Your 6 digit code</h1>
                        <h1>""" + str(numbers) + """</h1>
                    </div>
                    <br>
                    <div>
                        <h3>Hello """ + str(user.first_name) + """,</h3>
                        <p>You recently tried to recover your password. In order to recover your password, please use the above code.</p>
                        <br>
                        <p>If it wasn't you, please <a href="http://localhost:5000/settings">change your password.</a></p>
                    </div>
                    <br>
                    <div class="copyright" style="z-index: 10; color: rgb(129, 129, 129); text-decoration: none; background-color: #F1F1F1;">
                        © copyright 2022 Yarden Falik
                    </div>
                </body>
                </html>
            """

            part = MIMEText(html, "html")
            msg.attach(part)

            code = numbers

            # Create secure SMTP connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            flash('Email sent!', category = 'success')
        else:
            input = request.form.get('number')

            if input == numbers:
                print("success")
                print("input: " + str(input))
                print("numbers: " + str(numbers))
            else:
                print("error")
                print("input: " + str(input))
                print("numbers: " + str(numbers))

    return render_template('login/recover.html')

@auth.route('/addFriends', methods=['GET', 'POST'])
@login_required
def addFriends():
    if request.method == 'POST':
        temp = 2
        our_users = User.query.order_by(User.id)
        friends = Friend.query.order_by(Friend.id)
        name = request.form.get('name')
        for i in our_users:
            a = 0
            for j in friends:
                a+=1
            if(a==0 and i.first_name == name):
                new_Friend = Friend(name = name, userId = current_user.id, friendId = i.id)
                db.session.add(new_Friend)
                db.session.commit()
                flash(name + ' is now your friend', category='sucsses')
                temp = 1
                break
            for j in friends:
                if(i.first_name == name):
                    if (j.userId == current_user.id and j.name != name) or (j.userId != current_user.id):
                        new_Friend = Friend(name = name, userId = current_user.id, friendId = i.id)
                        db.session.add(new_Friend)
                        db.session.commit()
                        flash(name + ' is now your friend', category='sucsses')
                        temp = 1
                        break
                    else:
                        flash('this user is already your friend', category='error')
                        temp = 1
                        break
                else:
                    temp = 0    
        if temp == 0:
            flash('user not found', category='error')
        flash("temp =" + str(temp), category='error')

    return render_template('addFriends.html')

@auth.route('/addFriend/<name>')
@login_required
def addFriend(name):
    temp = 2
    our_users = User.query.order_by(User.id)
    friends = Friend.query.order_by(Friend.id)
    for i in our_users:
        a = 0
        for j in friends:
            a+=1
        if(a==0 and i.first_name == name):
            new_Friend = Friend(name = name, userId = current_user.id, friendId = i.id)
            db.session.add(new_Friend)
            db.session.commit()
            flash(name + ' is now your friend', category='sucsses')
            temp = 1
            break
        for j in friends:
            if(i.first_name == name):
                if (j.userId == current_user.id and j.name != name) or (j.userId != current_user.id):
                    new_Friend = Friend(name = name, userId = current_user.id, friendId = i.id)
                    db.session.add(new_Friend)
                    db.session.commit()
                    flash(name + ' is now your friend', category='sucsses')
                    temp = 1
                    break
                else:
                    flash('this user is already your friend', category='error')
                    temp = 1
                    break
            else:
                temp = 0    
    if temp == 0:
        flash('user not found', category='error')
    return redirect("/dashboard")

@auth.route('/deleteFriend/<first_name>')
@login_required
def deleteFriend(first_name):
    our_users = User.query.order_by(User.id)
    friends = Friend.query.order_by(Friend.id)

    Friend.query.filter_by(name = first_name).delete()
    db.session.commit()

    return redirect("/dashboard")

@auth.route('/user/<first_name>')
@login_required
def user(first_name):
    isFriend = 0
    our_users = User.query.order_by(User.id)
    for user in our_users:
        if user.first_name == first_name:
            oId = user.id
            if(len(str(user.id)) == 1):
                id = '000' + str(user.id)
            elif(len(str(user.id)) == 2):
                id = '00' + str(user.id)
            elif(len(str(user.id)) == 3):
                id = '0' + str(user.id)
            elif(len(str(user.id)) == 4):
                id = user.id
            email = user.email

    friends = Friend.query.order_by(Friend.id)
    for i in friends:
        if i.name == first_name and i.userId == current_user.id:
            isFriend = 1
    return render_template('user.html', oId = oId, name = first_name, id = id, email = email, isFriend = isFriend, friends = friends)

@auth.route('i_an')
@login_required
def counter1():
    file_add = "website/static/files/counter.txt"

    file = open(file_add, "r").read()

    if current_user.id == 1:
        return "<h1>"+ file +"</h1>"
    else:
        return redirect("/")

@auth.route('i')
def counter():
    file_add = "website/static/files/counter.txt"

    file = open(file_add, "r").read()
    num = int(file)

    f = open(file_add, "w")
    f.write(str(num + 1))
    f.close()

    file = open(file_add, "r").read()

    return redirect("/")

@auth.route('/pictures/<first_name>')
@login_required
def pictures(first_name):
    picture = User.query.filter_by(first_name = first_name).first()
    return send_file(BytesIO(picture.pictureData), attachment_filename="picture.png", as_attachment=True)