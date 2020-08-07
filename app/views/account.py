from flask import Blueprint, render_template, jsonify
from ..models.model import *


account = Blueprint('account', __name__)

