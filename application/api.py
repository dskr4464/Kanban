from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse

from application.database import db
from application.models import *
from application.validation import *
from datetime import datetime

card_fields = {
  "card_id" : fields.Integer,
  "title" : fields.String,
  "content" : fields.String,
  "deadline" : fields.String,
  "completed_flag" : fields.Integer,
  "create_time" : fields.String,
  "last_update" : fields.String,
  "late" : fields.Integer,
  "list_id" : fields.Integer
}

list_fields = {
  "list_id" : fields.Integer,
  "list_name" : fields.String,
  "user_id" : fields.Integer,
  "cards" : fields.List(fields.Nested(card_fields))
}

user_fields = {
  "user_id" : fields.Integer,
  "user_name" : fields.String,
  "lists" : fields.List(fields.Nested(list_fields))
}

create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument("list_name")

create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument("title")
create_card_parser.add_argument("content")
create_card_parser.add_argument("deadline")

def list_present(user,list_name):
  flag=0
  for x in user.lists:
    if x.list_name==list_name:
      flag=1
      break
  return flag

def card_present(list,title):
  flag=0
  for x in list.cards:
    if x.title==title:
      flag=1
      break
  return flag

class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self,user_name):
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            return user
        else:
            raise NotFoundError(status_code=404,error_msg="User Not Found")

class ListAPI(Resource):
  @marshal_with(list_fields)
  def get(self,user_name,list_name):
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    if list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    return list

  @marshal_with(list_fields)
  def put(self,user_name,list_name):
    args = create_list_parser.parse_args()
    new_list_name = args.get("list_name", None)
    print(new_list_name==None)
    if new_list_name==None or new_list_name=="":
      raise BusinessValidationError(status_code=400,error_code="BE2001",error_msg="Listname is required")
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    if list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    if list_present(user,new_list_name)==1:
      raise BusinessValidationError(status_code=400,error_code="BE2002",error_msg="Duplicate list is found")
    list.list_name=new_list_name
    db.session.commit()
    return list

  def delete(self,user_name,list_name):
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    if list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    if len(list.cards)>0:
      raise BusinessValidationError(status_code=400,error_code="BE2003",error_msg="List contains cards, either move or delete the cards first to delete the list")
    db.session.delete(list)
    db.session.commit()
    return "List is successfully deleted."
  
  @marshal_with(list_fields)
  def post(self,user_name):
    args = create_list_parser.parse_args()
    list_name = args.get("list_name", None)
    if list_name==None or list_name=="":
      raise BusinessValidationError(status_code=400,error_code="BE2001",error_msg="Listname is required")
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    if list_present(user,list_name)==1:
      raise BusinessValidationError(status_code=400,error_code="BE2002",error_msg="Duplicate list is found")
    new_list = List(list_name=list_name,user_id=user.user_id)
    db.session.add(new_list)
    db.session.commit()
    return new_list
    
  
class CardAPI(Resource):
  @marshal_with(card_fields)
  def get(self,user_name,list_name,title):
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    if list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    card = Card.query.filter_by(list_id=list.list_id, title=title).first()
    if card==None:
      raise NotFoundError(status_code=404,error_msg="Card Not Found")
    if datetime.strptime(card.deadline, "%B %d, %Y %H:%M:%S") < datetime.now():
      card.late=1
    db.session.commit()
    return card
  @marshal_with(card_fields)
  def put(self,user_name,list_name,title):
    args = create_card_parser.parse_args()
    new_title = args.get("title", None)
    content = args.get("content", None)
    deadline = args.get("deadline", None)
    dl_str = ""
    if new_title=="":
      raise BusinessValidationError(status_code=400,error_code="BE3001",error_msg="Cardtitle is required")
    if deadline==None or deadline=="":
      raise BusinessValidationError(status_code=400,error_code="BE3002",error_msg="Deadline is required")
    else:
      try:
        dl = datetime.strptime(deadline, '%d-%m-%Y')
      except:
        raise BusinessValidationError(status_code=400,error_code="BE3003",error_msg="Deadline is not in required format. Format should be DD-MM-YYYY")
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    if list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    card = Card.query.filter_by(list_id=list.list_id, title=title).first()
    if card==None:
      raise NotFoundError(status_code=404,error_msg="Card Not Found")
    db.session.delete(card)
    db.session.commit()
    if card_present(list, new_title)==1:
      raise BusinessValidationError(status_code=400,error_code="BE3004",error_msg="Duplicate card is found in the list")
    dl_str = dl.strftime("%B %d, %Y %H:%M:%S")
    d_str = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    new_card = Card(title=new_title,content=card.content,deadline=dl_str,create_time=card.create_time,last_update=d_str,list_id=list.list_id)
    if content!=None:
      new_card.content=content
    if dl < datetime.now():
      new_card.late=1
    db.session.add(new_card)
    db.session.commit()
    return new_card
  def delete(self,user_name,list_name,title):
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    if list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    card = Card.query.filter_by(list_id=list.list_id, title=title).first()
    if card==None:
      raise NotFoundError(status_code=404,error_msg="Card Not Found")
    db.session.delete(card)
    db.session.commit()
    return "Card is successfully deleted."
    
  @marshal_with(card_fields)
  def post(self,user_name,list_name):
    args = create_card_parser.parse_args()
    title = args.get("title", None)
    content = args.get("content", None)
    deadline = args.get("deadline", None)
    dl_str = ""
    if title==None or title=="":
      raise BusinessValidationError(status_code=400,error_code="BE3001",error_msg="Cardtitle is required")
    if deadline==None or deadline=="":
      raise BusinessValidationError(status_code=400,error_code="BE3002",error_msg="Deadline is required")
    else:
      try:
        dl = datetime.strptime(deadline, '%d-%m-%Y')
      except:
        raise BusinessValidationError(status_code=400,error_code="BE3003",error_msg="Deadline is not in required format. Format should be DD-MM-YYYY")
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    if list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    if card_present(list, title)==1:
      raise BusinessValidationError(status_code=400,error_code="BE3004",error_msg="Duplicate card is found in the list")
    dl_str = dl.strftime("%B %d, %Y %H:%M:%S")
    d_str = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    new_card = Card(title=title,content=content,deadline=dl_str,create_time=d_str,last_update=d_str,list_id=list.list_id)
    if dl < datetime.now():
      new_card.late=1
    db.session.add(new_card)
    db.session.commit()
    return new_card

class MoveCardAPI(Resource):
  @marshal_with(card_fields)
  def put(self,user_name,list_name,title):
    args = create_list_parser.parse_args()
    new_list_name = args.get("list_name", None)
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    new_list = List.query.filter_by(user_id=user.user_id, list_name=new_list_name).first()
    if list==None or new_list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    card = Card.query.filter_by(list_id=list.list_id, title=title).first()
    if card==None:
      raise NotFoundError(status_code=404,error_msg="Card Not Found")
    if card_present(new_list, title)==1:
      raise BusinessValidationError(status_code=400,error_code="BE3004",error_msg="Duplicate card is found in the list")
    d_str = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    card.list_id=new_list.list_id
    card.last_update=d_str
    if datetime.strptime(card.deadline, "%B %d, %Y %H:%M:%S") < datetime.now():
      card.late=1
    db.session.commit()
    return card

class MoveListAPI(Resource):
  @marshal_with(user_fields)
  def put(self,user_name,list_name):
    args = create_list_parser.parse_args()
    new_list_name = args.get("list_name", None)
    user = User.query.filter_by(user_name=user_name).first()
    if user==None:
      raise NotFoundError(status_code=404,error_msg="User Not Found")
    list = List.query.filter_by(user_id=user.user_id, list_name=list_name).first()
    new_list = List.query.filter_by(user_id=user.user_id, list_name=new_list_name).first()
    if list==None or new_list==None:
      raise NotFoundError(status_code=404,error_msg="List Not Found")
    for x in list.cards:
      if card_present(new_list, x.title)==1:
        raise BusinessValidationError(status_code=400,error_code="BE3004",error_msg="Duplicate card is found in the list")
    for x in list.cards:
      x.list_id = new_list.list_id
      if datetime.strptime(x.deadline, "%B %d, %Y %H:%M:%S") < datetime.now():
        x.late=1
    db.session.commit()
    return user