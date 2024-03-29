## views.py inside post folder
# -*- coding: utf-8 -*-


from flask import (Blueprint, render_template, url_for,
                   flash, redirect, request, abort)
from eduka import login_manager, db
from eduka.posts.post_form import AddPostForm
from flask_login import login_required, current_user
from eduka.models import User, Post, PostLink, PostView

from eduka.utils.database_utils import (saving_post, add_tags, saving_links,
                                        saving_views, update_nbr_views,
                                        update_links)
from eduka.utils.other_utils import populate_form
from datetime import datetime as dt, timedelta

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates/posts')


@posts_blueprint.route('/publier', methods=['GET','POST'])
@login_required
def add_post():

    title = 'Écrire votre publication'
    ## adding 7 days for the end date
    seven_days = timedelta(days=7)

    form = AddPostForm()

    form.start_date.data = dt.now();
    form.end_date.data = dt.now() + seven_days;

    if form.validate():
        pass
        ##print('******* is valid!')

    if form.validate_on_submit():
        ###print('Has validated on submit')

        author_id = current_user.id;

        title = form.post_title.data;
        summary = form.post_summary.data;
        start_date = form.start_date.data;
        end_date = form.end_date.data;
        level_beg = form.start_level.data;
        level_end = form.end_level.data;
        post_tags = form.post_tags.data;
        privacy_level = form.post_privacy.data;

        ## to get the links and titles
        post_link_titles = request.form.getlist('link1_title');
        post_links = request.form.getlist('link1')

        ## save the post without the links
        post = Post(title=title, summary=summary,
                    date_start=start_date, date_end=end_date,
                    level_beg=level_beg, level_end=level_end,
                    privacy_level=privacy_level, user_id=author_id)

        ## saving posts using the database_utils
        saving_post(post)

        # removing all the spaces
        post_tags.split(", ")
        tags = post_tags.split(",")
        for tag in tags:
            n_tag = ''.join(tag.split())
            post_tag = add_tags(n_tag.lower())
            print(post_tag)
            post.tags.append(post_tag)

        db.session.commit()

        ## saving links
        saving_links(links=post_links, titles=post_link_titles, post_id=post.id)
        ## saving the number of views
        saving_views(post_id=post.id)



        ## empty the fieldsof the form
        form.post_title.data = '';
        form.post_summary.data = '';
        form.start_date.data = dt.now();
        form.end_date.data = dt.now() + seven_days;
        form.start_level.data = 'bg';
        form.end_level.data = 'exp';
        form.post_privacy.data = 'pbl';

        flash (u'New Post Created!', 'is-success')

        return redirect(url_for('posts.add_post'))

    #print(f'form errors: {form.errors}')

    return render_template('create_post.html', title=title, form=form)



@posts_blueprint.route('/post/<string:post_public_id>')
def show_post(post_public_id):

    ## let get the post

    post = Post.query.filter(Post.public_id==post_public_id).first_or_404()
    author = User.query.filter(User.id == post.user_id).first_or_404()
    postlinks = post.links
    views = 0
    ## check to see if the
    if post.nbr_views:
        views = post.nbr_views[0].nbr_views
        views+=1
    else:
        views = 1
        ## adding number of views for the page
        saving_views(post_id=post.id)

    ## get all the Tag objects for the post
    tags_obj = post.tags
    ##print(f'tags: {post.tags}')
    tags = []
    for t in tags_obj:
        tags.append(t.name)



    #tags = tags_str.split(",")
    ##print(f"tags: {tags}")
    title = post.title

    ## updated the database with the new number of views
    ## adding number of views for the page

    update_nbr_views(post.id)

    return render_template('post.html', title=title, post=post,
                           links=postlinks, author=author, views=views, tags=tags)





@posts_blueprint.route('/update/<string:post_public_id>',methods=['GET', 'POST'])
@login_required
def update_post(post_public_id):
    form = AddPostForm()
    post = Post.query.filter(Post.public_id==post_public_id).first_or_404()
    nbr_links = len(post.links)

    if current_user.id != post.user_id:
        ## the if statement here, makes sure that only the author can update the post
        ## print(f'current user id: {current_user.id}, post author id: {post.user_id}')
        return redirect(url_for('posts.show_post', post_id=post.id))

    ## call the populate form from the utils module
    populate_form(post=post, form=form)

    ##### check and submit the form #####
    ## only update the content and title here
    ## need to change the database relationships
    if form.validate_on_submit():
        ''' saving the post '''
        ## to get the links and titles
        new_links = {
            'l_titles': request.form.getlist('link1_title'),
            'links': request.form.getlist('link1')
        }
        #post_link_titles = request.form.getlist('link1_title');
        #post_links = request.form.getlist('link1')

        ## save the post without the links
        post.title = request.form['post_title']
        post.summary = request.form['post_summary']
        post.start_date = request.form['start_date']
        post.end_date = request.form['end_date']
        post.level_beg = request.form['start_level']
        post.level_end = request.form['end_level']
        post_tags = request.form['post_tags']
        post.privacy_level = request.form['post_privacy']
        post.date_updated = dt.utcnow()
        ## updating tags
        tags = post_tags.split(", ")
        for tag in tags:
            #tag.strip()
            ## to remove all whitespaces
            n_tag = ''.join(tag.split())
            post_tag = add_tags(n_tag.lower())
            print(post_tag)
            post.tags.append(post_tag)

        db.session.commit()

        ## check to see if there have been changes and save links
        ## if necessary
        update_links(post_links=post.links,
                     new_links=new_links, post_id=post.id)

        ### do a return to the post view page
        return redirect(url_for('posts.show_post',
                                post_public_id=post.public_id))


    return render_template('update_post.html', form=form,
                           nbr_links=nbr_links, post=post)



@posts_blueprint.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    pass
