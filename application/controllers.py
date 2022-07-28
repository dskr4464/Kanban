from jinja2 import Template
from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask import current_app as app
from datetime import datetime
from application.models import *
import json

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        info = request.form
        user = User.query.filter_by(user_name=info["username"]).first()
        temp = Template("/user/{{ id }}")

        return redirect(temp.render(id=user.user_id))

@app.route("/user/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        try:
            info = request.form
            new_user = User(user_name=info["username"])
            db.session.add(new_user)
        except:
            print("Rolling back")
            db.session.rollback()
        else:
            db.session.commit()
            return redirect("/")

@app.route("/user/<id>", methods=["GET", "POST"])
def login(id):
    if request.method == "GET":
        user = User.query.filter_by(user_id=id).first()
        list = List.query.filter_by(user_id=id).all()
        count=0
        for x in user.lists:
            for y in x.cards:
                if y.completed_flag==0:
                    count+=1
                d = datetime.strptime(y.deadline, "%B %d, %Y %H:%M:%S")
                if datetime.now() > d:
                    y.late=1
                    db.session.commit()
        
        return render_template("user.html",user=user,list=list,count=count)
    else:
        info = request.form
        list = List(list_name=info["name"],user_id=id)
        db.session.add(list)
        db.session.commit()
        temp = Template("/user/{{ id }}")

        return redirect(temp.render(id=id))

@app.route("/user/<user_id>/<list_id>/<list_name>/add-card", methods=["GET", "POST"])
def add_card(user_id,list_id,list_name):
    if request.method == "POST":
        info = request.form
        x = info["deadline"]
        d1 = datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]))
        d2 = datetime.now()
        d1_str = d1.strftime("%B %d, %Y %H:%M:%S")
        d2_str = d2.strftime("%B %d, %Y %H:%M:%S")
        card = Card(title=info["title"],content=info["content"],deadline=d1_str,create_time=d2_str,last_update=d2_str,list_id=list_id)
        db.session.add(card)
        db.session.commit()
        temp = Template("/user/{{ id }}")

        return redirect(temp.render(id=user_id))

@app.route("/user/<user_id>/<list_id>/<list_name>/edit-list", methods=["GET", "POST"])
def edit_list(user_id,list_id,list_name):
    if request.method == "POST":
        info = request.form
        list = List.query.filter_by(list_id=list_id).first()
        list.list_name = info["name"]
        db.session.commit()
        temp = Template("/user/{{ id }}")

        return redirect(temp.render(id=user_id))

@app.route("/user/<user_id>/<list_id>/delete", methods=["GET", "POST"])
def delete_list(user_id,list_id):
    if request.method == "GET":
        cards = Card.query.filter_by(list_id=list_id).all()
        for x in cards:
            db.session.delete(x)
        list = List.query.filter_by(list_id=list_id).first()
        db.session.delete(list)
        db.session.commit()

    else:
        info = request.form
        if info["exampleRadios"]=="option1":
            list = List.query.filter_by(list_name=info["list_name"], user_id=user_id).first()
            cards = Card.query.filter_by(list_id=list_id).all()
            try:
                for x in cards:
                    db.session.delete(x)
                    x.list_id=list.list_id
                    db.session.add(x)
                list = List.query.filter_by(list_id=list_id).first()
                db.session.delete(list)
            except:
                db.session.rollback()
            finally:
                db.session.commit()
        else:
            cards = Card.query.filter_by(list_id=list_id).all()
            for x in cards:
                db.session.delete(x)
            list = List.query.filter_by(list_id=list_id).first()
            db.session.delete(list)
            db.session.commit()
    temp = Template("/user/{{ id }}")

    return redirect(temp.render(id=user_id))

@app.route("/user/<user_id>/<list_id>/<card_id>/edit-card", methods=["GET", "POST"])
def edit_card(user_id,list_id,card_id):
    if request.method == "POST":
        info = request.form
        card = Card.query.filter_by(card_id=card_id).first()
        card.title = info["title"]
        card.content = info["content"]
        d2 = datetime.now()
        d2_str = d2.strftime("%B %d, %Y %H:%M:%S")
        card.last_update = d2_str
        db.session.commit()
        temp = Template("/user/{{ id }}")

        return redirect(temp.render(id=user_id))

@app.route("/user/<user_id>/<list_id>/<card_id>/delete", methods=["GET", "POST"])
def delete_card(user_id,list_id,card_id):
    if request.method == "GET":
        card = Card.query.filter_by(card_id=card_id).first()
        db.session.delete(card)
        db.session.commit()
        temp = Template("/user/{{ id }}")

        return redirect(temp.render(id=user_id))

@app.route("/user/<user_id>/<list_id>/<card_id>/move", methods=["GET", "POST"])
def move_card(user_id,list_id,card_id):
    if request.method == "POST":
        info = request.form
        list = List.query.filter_by(list_name=info["new list_name"], user_id=user_id).first()
        card = Card.query.filter_by(card_id=card_id).first()
        db.session.delete(card)
        card.list_id=list.list_id
        try:
            db.session.add(card)
        except:
            db.session.rollback()
        else:
            db.session.commit()
        temp = Template("/user/{{ id }}")

        return redirect(temp.render(id=user_id))

@app.route("/user/<user_id>/<list_id>/<card_id>/<flag>/flag", methods=["GET", "POST"])
def flag(user_id,list_id,card_id,flag):
    if request.method == "GET":
        card = Card.query.filter_by(card_id=card_id).first()
        card.completed_flag = int(flag)
        db.session.commit()
        temp = Template("/user/{{ id }}")
        
        return redirect(temp.render(id=user_id))
    else:
        temp = Template("/user/{{ id }}")
        
        return redirect(temp.render(id=user_id))

@app.route("/user/<id>/summary", methods=["GET", "POST"])
def summary(id):
    if request.method == "GET":
        user = User.query.filter_by(user_id=id).first()
        list = List.query.filter_by(user_id=id).all()
        dict={}
        count=0
        for x in user.lists:
            m=[0,0,0,0,0]
            for y in x.cards:
                m[0]+=1
                if y.completed_flag==0:
                    count+=1
                    if y.late==1:
                        m[4]+=1
                    else:
                        m[2]+=1
                else:
                    if y.late==1:
                        m[3]+=1
                    else:
                        m[1]+=1
            dict[x.list_id] = m

        return render_template("summary.html",user=user,ginfo=dict,count=count)    

@app.route("/user/<id>/find/<name>", methods=["GET", "POST"])
def find_list(id,name):
    user = User.query.filter_by(user_id=id).first()
    for x in user.lists:
        if x.list_name==name:
            return "OK",200
    return "NOT OK",202

@app.route("/find/<name>", methods=["GET", "POST"])
def find_user(name):
    users = User.query.all()
    for x in users:
        if x.user_name==name:
            return "OK",200
    return "NOT OK",202

@app.route("/user/<user_id>/<title>/find/card/<name>", methods=["GET", "POST"])
def find_card(user_id,title,name):
    list = List.query.filter_by(user_id=user_id, list_name=name).first()

    if(list==None):
        return "NO LIST",202

    for x in list.cards:
        if x.title==title:
            return "NOT OK",203
    return "OK",200

@app.route("/user/<user_id>/<list_id>/compare/list/<name>", methods=["GET", "POST"])
def compare_list(user_id,list_id,name):
    list1 = List.query.filter_by(user_id=user_id, list_name=name).first()
    list2 = List.query.filter_by(user_id=user_id, list_id=list_id).first()

    if(list1==None):
        return "NO LIST",202

    for x in list1.cards:
        for y in list2.cards:
            if x.title==y.title:
                return "NOT OK",203
    return "OK",200