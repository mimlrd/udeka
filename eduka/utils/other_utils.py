## create utils for the app
# -*- coding: utf-8 -*-

from flask import Blueprint


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def populate_form(post, form):

    ## fill the form with info from the post to update

    form.post_title.data = post.title;
    form.post_summary.data = post.summary;
    form.start_date.data = post.date_start;
    form.end_date.data = post.date_end;
    form.start_level.data = post.level_beg;
    form.end_level.data = post.level_end;
    form.post_privacy.data = post.privacy_level

    tags = []
    for t in post.tags:
        tags.append(t.name)
    ## using ", ".join() to transform the list into a
    ## string separated by a comma (,)
    form.post_tags.data = ", ".join(tags)

def populate_edit_form(user,form):

    ## populate all the data in the edit pages
    form.username.data = user.username
    form.email.data = user.email
    form.bio.data = user.bio
