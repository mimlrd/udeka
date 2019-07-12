## views.py in core
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, flash
from eduka.models import Post



core_blueprint = Blueprint('core',
                            __name__,
                            template_folder='templates/core',
                            static_url_path='/core/static',
                            static_folder='static')


@core_blueprint.route('/')
def home():
    title = 'eduka! Apprendre mieux!'


    return render_template('home.html', title=title)


@core_blueprint.route('/about')
def about():
    title = 'eduka! À propos de nous'
    return render_template('about.html', title=title)

@core_blueprint.route('/collections')
def show_collections():
    title = 'eduka! | Public collections disponible'

    ## get all the public posts

    p = Post.query.filter(Post.privacy_level == 'pbl')
    p_desc = p.order_by(Post.date_posted.desc())
    posts = p_desc.limit(50).all()

    return render_template('collection.html', title=title, posts=posts)
