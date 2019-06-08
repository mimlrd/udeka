## database_utils.py

'''
 A utils to interact with the database.
 Here we will put the different functions to interact ith the database
'''
from eduka import db
from eduka.models import User, Post, PostLink, PostView


## saving post to database
def saving_post(post):
    ## save the post without the links
    ## saving into database
    db.session.add(post)
    db.session.commit()


## saving post links
def saving_links(links, titles, post_id):

    ## saving the links
    postLinks = []
    for lk, t in zip(links, titles):
        ## to know if the link is not empty
        if lk and len(lk.strip()) > 0:
            p_links = PostLink(link_title=t, link_url=lk , post_id=post_id)
            postLinks.append(p_links)


    ##print(f" ***** Links are:  {postLinks}")
    ## save links to database
    db.session.add_all(postLinks)
    db.session.commit()


## saving the number of views

def saving_views(post_id):

    ## adding number of views for the page
    nbr_view = PostView(post_id=post_id)
    ## save number of view to database
    db.session.add(nbr_view)
    db.session.commit()



def update_nbr_views(post_id):
    ## get the post views
    nbr_views = PostView.query.filter(PostView.post_id == post_id).first()
    ## update the number of nbr_views
    nbr_views.nbr_views += 1
    ## save number of view to database
    db.session.add(nbr_views)
    db.session.commit()
