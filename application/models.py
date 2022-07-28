from .database import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    lists = db.relationship("List")

class List(db.Model):
    __tablename__ = "list"
    __table_args__ = ( db.UniqueConstraint('list_name','user_id'), )
    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    cards = db.relationship("Card")

class Card(db.Model):
    __tablename__ = "card"
    __table_args__ = ( db.UniqueConstraint('title','list_id'), )
    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)
    completed_flag = db.Column(db.Integer, nullable=False, default=0)
    create_time = db.Column(db.String, nullable=False)
    last_update = db.Column(db.String, nullable=False)
    late = db.Column(db.Integer, nullable=False, default=0)
    list_id = db.Column(db.Integer, db.ForeignKey("list.list_id"), nullable=False)
