print("USER.module.py在", __name__)

from flask import Blueprint
from ..models.model import *


USER = Blueprint('USER', __name__)

@USER.route('/<name>')
def index(name):
    data = account.query.filter_by(userID = 'ddd').first()
    print(data)
    return 'Welcome ' + name