## views.py in core

from flask import Blueprint, render_template, redirect, flash


core_blueprint = Blueprint('core',
                            __name__,
                            template_folder='templates/core')


@core_blueprint.route('/')
def home():
    title = 'eduka! Apprendre mieux!'
    return render_template('home.html', title=title)


@core_blueprint.route('/about')
def about():
    title = 'eduka! À propos de nous'
    return render_template('about.html', title=title)
