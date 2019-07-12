## create filters for the app
# -*- coding: utf-8 -*-
from datetime import datetime as dt
#from app import app

from flask import Blueprint
import arrow

filter_blueprint = Blueprint('my_filters', __name__, template_folder=None)



## date formating
@filter_blueprint.app_template_filter()
def format_date(d):
    ## tuto: https://www.michaelcho.me/article/custom-jinja-template-filters-in-flask
    ##### will need to use moments.js instead
    ##### see tutorials:
    ## https://code.tutsplus.com/tutorials/templating-with-jinja2-in-flask-date-and-time-formatting-with-momentjs--cms-25813
    return d.strftime("%a %d %B %Y")



@filter_blueprint.app_template_filter()
def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()
