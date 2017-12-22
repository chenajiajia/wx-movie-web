from flask import Blueprint

movie = Blueprint('movie', __name__)

from . import getMovies,getTv,getSubjectDetail