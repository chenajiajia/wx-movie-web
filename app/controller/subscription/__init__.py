from flask import Blueprint

subscription = Blueprint('subscription', __name__)

from . import getSubscription,subscribe