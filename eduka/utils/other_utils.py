## create utils for the app

from flask import Blueprint

def populate_form(post, form):

    ## fill the form with info from the post to update

    form.post_title.data = post.title;
    form.post_summary.data = post.summary;
    form.start_date.data = post.date_start;
    form.end_date.data = post.date_end;
    form.start_level.data = post.level_beg;
    form.end_level.data = post.level_end;
    form.post_category.data = post.category


    ## adding the links and titles
    '''
    for i,l in enumerate(post.links):

        form.link1_title.data = l.link_title;
        form.link1.data = l.link_url;

    '''
