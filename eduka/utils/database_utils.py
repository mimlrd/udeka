## database_utils.py

'''
 A utils to interact with the database.
 Here we will put the different functions to interact ith the database
'''
from eduka import db
from eduka.models import User, Post, PostLink, PostView, Tag


## saving post to database
def saving_post(post):
    ## save the post without the links
    ## saving into database
    db.session.add(post)
    db.session.commit()

## get the tags
def add_tags(tag):
    existing_tag = Tag.query.filter(Tag.name == tag.lower().strip()).one_or_none()
    """if it does return existing tag objec to list"""
    if existing_tag is not None:
        return existing_tag
    else:
       new_tag = Tag()
       new_tag.name = tag.lower()
       return new_tag


## saving post links
def saving_links(links, titles, post_id):
    ##print('in saving links')

    ## saving the links
    postLinks = []
    for lk, t in zip(links, titles):
        ## to know if the link is not empty
        if lk and len(lk.strip()) > 0:
            ##print(f'lk is: {lk}')
            p_links = PostLink(link_title=t, link_url=lk , post_id=post_id)
            postLinks.append(p_links)


    ##print(f" ***** Links are:  {postLinks}")
    ## save links to database
    db.session.add_all(postLinks)
    db.session.commit()

## updating links
def update_links(post_links, new_links, post_id):
    ## get the links from the dictionaries
    ## I WILL NEED TO CREATE A DIFF CALCULATOR ALGORITHM
    ## get the previous links
    pr_links = []
    pr_link_titles = []

    for l in post_links:
        pr_links.append(l.link_url)
        pr_link_titles.append(l.link_title)

    ## to get the links and titles
    old_links = {
        'l_titles': pr_link_titles,
        'links': pr_links
    }


    ## new links
    n_link_titles = new_links['l_titles']
    n_links = new_links['links']

    ## check to see if the links are different
    ## if there has been any changes or new links added
    ## using symmetric difference, we will find the values
    ## that are unique in both new and old links and titles

    ## verify thath there have been old links and new links
    if old_links is not None and new_links is not None:
        '''Post has old links user mights have updated them '''
        ## get the unique elements in each list
        titles_symm = list(set(pr_link_titles).symmetric_difference(n_link_titles))
        links_symm = list(set(pr_links).symmetric_difference(n_links))

        ## get the links and titles which are unique
        u_titles = list(set(n_link_titles) - set(pr_link_titles))
        u_links = list(set(n_links) - set(pr_links))
        ##print('Case 1 - ---')
        ##print(f'unique titles: {u_titles}')
        ##print(f'unique links: {u_links}')

        ## now we can save the links
        ## saving the links
        saving_links(links=u_links, titles=u_titles, post_id=post_id)



    elif old_links is not None and new_links is None:
        ''' User has deleted all the links '''
        ##print('Case 2 - ---')
        ##print(f'post links: {post_links}')
        ## delete old links
        for l in post_links:
            try:
                db.session.delete(l)
                db.session.commit()
            except:
                db.session.rollback()


    elif old_links is None and new_links is not None:
        ''' User has added new links '''
        ##print('Case 3 - ---')
        ##print(f'post links: {new_links}')
        ## save new links
        saving_links(links=n_links, titles=n_link_titles,
                     post_id=pos_id)








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
