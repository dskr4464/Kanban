import json
from werkzeug.exceptions import HTTPException
from flask import make_response

class NotFoundError(HTTPException):
  def __init__(self, error_msg, status_code):
    msg = {"error_message":error_msg}
    self.response = make_response(json.dumps(msg), status_code)

class BusinessValidationError(HTTPException):
  def __init__(self, error_msg, status_code, error_code):
    msg = {"error_code" : error_code, "error_message" : error_msg}
    self.response = make_response(json.dumps(msg), status_code)