## create filters for the app
from datetime import datetime as dt
#from app import app

from flask import Blueprint

filter_blueprint = Blueprint('my_filters', __name__, template_folder=None)



## date formating
@filter_blueprint.app_template_filter()
def format_date(d):
    ## tuto: https://www.michaelcho.me/article/custom-jinja-template-filters-in-flask
    ##### will need to use moments.js instead
    ##### see tutorials:
    ## https://code.tutsplus.com/tutorials/templating-with-jinja2-in-flask-date-and-time-formatting-with-momentjs--cms-25813
    return d.strftime("%a %d %B %Y")
