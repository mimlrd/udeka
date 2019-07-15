## models.py
# -*- coding: utf-8 -*-


from eduka import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime as dt
import shortuuid


##load the current user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class PostClap(db.Model):

    '''
    Adding social to the post, allow users to like a post
    '''
    __tablename__ = 'postclaps'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=dt.utcnow)


class User(db.Model, UserMixin):

    '''
    User class that will determine ...
    '''
    DEFAULT_BIO = "Utilisateur n'a pas encore ajouter un bio "
    DEFAULT_PROFILE_LINK = "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"
    USR_PUBLIC_IDX = str(shortuuid.uuid())

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(80), unique=True,
                          index=True, default=USR_PUBLIC_IDX)
    profile_image_link = db.Column(db.String(350), nullable=True,
                                    default=DEFAULT_PROFILE_LINK)
    email = db.Column(db.String(80), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    bio = db.Column(db.Text(), default=DEFAULT_BIO)
    member_since = db.Column(db.DateTime(), default=dt.utcnow)
    updated_date = db.Column(db.DateTime(), default=dt.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    ## see following links:
    ## https://github.com/miguelgrinberg/flasky/blob/master/app/models.py
    hash_password = db.Column(db.String(256))
    # This connects Posts to a User Author.
    posts = db.relationship('Post', backref='author', lazy=True)

    liked = db.relationship('PostClap',
                            foreign_keys=[PostClap.user_id],
                            backref='user',
                            lazy='dynamic',
                            cascade='all, delete-orphan')




    def __init__(self, email, username, pwd, bio=None, profile_image_link=None):
        #self.public_id = self.__create_public_id()
        self.email = email.lower()
        self.username = username.lower()
        self.bio = bio
        self.profile_image_link = profile_image_link
        self.hash_password = generate_password_hash(pwd, method="sha256")
        #self.updated_date = dt.utcnow

        if self.public_id is None:
            # print("setting public_id")
            self.public_id = str(shortuuid.uuid())

    @staticmethod
    def __create_public_id():
        if User.public_id is None:
            return str(shortuuid.uuid())

    def __repr__(self):
        return f'Username: {self.username} and email: {self.email}'

    def check_password(self, pwd):
        return check_password_hash(self.hash_password, pwd)

    def clap_post(self, post):
        if not self.had_clapped_post(post):
            like = PostClap(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unclap_post(self, post):
        if self.had_clapped_post(post):
            PostClap.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def had_clapped_post(self, post):
        return PostClap.query.filter(
            PostClap.user_id == self.id,
            PostClap.post_id == post.id).count() > 0

class AnonimousUser(AnonymousUserMixin):

    def __init__(self):
        self.username = 'Guest'

    def had_clapped_post(self, post):
        return 0

login_manager.anonymous_user = AnonimousUser


class Post(db.Model):

    # Setup the relationship to the User table
    users = db.relationship(User)

    '''
    Post class will determine how the user add a post.
    '''
    __tablename__ = 'posts'

    DEFAULT_POST_IMG_LINK = "https://cdn.pixabay.com/photo/2019/05/01/21/39/programming-4172154_960_720.jpg"
    POST_PUBLIC_IDX = str(shortuuid.uuid())

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(80),
                          unique=True, default=POST_PUBLIC_IDX)

    date_posted = db.Column(db.DateTime, index=True, default=dt.utcnow)
    date_updated = db.Column(db.DateTime(), default=dt.utcnow)
    title = db.Column(db.String(200), unique=False, nullable=False)
    summary = db.Column(db.Text(), nullable=False)
    date_start = db.Column(db.DateTime, default=dt.utcnow)
    ## need to find a way to automatically add 7 days to starte date as default
    date_end = db.Column(db.DateTime, default=dt.utcnow)
    level_beg = db.Column(db.String(6), default='bg')
    level_end = db.Column(db.String(6), default='bg')
    privacy_level = db.Column(db.String(6), index=True ,default='pbl')


    ## level ( bg- beginner, intr- intermediate, adv- Advance, exp- expert)

    ##---> Rename category - tags (might need to create own table Tag)
    ##---> tags need to be indexed, so users could search (query) easily by tag
    ##category = db.Column(db.String(), default='IT')
    post_image_link = db.Column(db.String(350), nullable=True,
                                default=DEFAULT_POST_IMG_LINK)
    ##nbr_views = db.Column(db.Integer, default=0)
    # Connect this table with other tables such as users and links
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.relationship('Tag', secondary='post_tags', lazy='subquery',
                           backref=db.backref('posts', lazy=True))
    links = db.relationship('PostLink', backref='post_link', lazy=True)
    nbr_views = db.relationship('PostView', backref='post_view', lazy=True)
    claps = db.relationship('PostClap', backref='post', lazy='dynamic')


    def __init__(self, title, summary,level_beg,
                 level_end, privacy_level, user_id, date_end, date_start=None):

        self.title = title;
        self.summary = summary;
        self.date_start = date_start;
        self.date_end = date_end;
        self.level_beg = level_beg;
        self.level_end = level_end;
        self.privacy_level = privacy_level;
        self.user_id = user_id
        #self.date_updated = dt.utcnow

        if self.public_id is None:
            self.public_id = str(shortuuid.uuid())

    def __repr__(self):
        return f'Post title: {self.title} and started at level:{self.level_beg}'


class Tag(db.Model):
    ''' The tags table for a many-to-many relationship '''
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), default='Python')

    def __repr__(self):
        return self.name

## mapping table
post_tags = db.Table('post_tags', db.Model.metadata,
                db.Column('tag_id', db.Integer,
                          db.ForeignKey('tags.id'),
                          primary_key=True),
                db.Column('post_id', db.Integer,
                          db.ForeignKey('posts.id'),
                          primary_key=True)
                )




class PostLink(db.Model):
    '''
    The post links here.
    '''

    # Setup the relationship to the User table
    posts = db.relationship(Post)

    __tablename__ = 'postlinks'

    id = db.Column(db.Integer, primary_key=True)
    link_title = db.Column(db.String(200), nullable=False)
    link_url = db.Column(db.String(), unique=False, nullable=False)
    ## create the relation between the Posts Table with the Links table
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)


    def __init__(self, link_title, link_url, post_id):
        self.link_title = link_title;
        self.link_url = link_url;
        self.post_id = post_id;

    def __repr__(self):
        return f'Post id:{self.post_id} and link is: {self.link_url}'


class PostView(db.Model):

    posts = db.relationship(Post)
    '''
    Get the count of the number of views that the user has view a post
    '''

    __tablename__ = 'postviews'

    id = db.Column(db.Integer, primary_key=True)
    nbr_views = db.Column(db.Integer, default=0)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, post_id):
        self.post_id = post_id

        if self.nbr_views is None:
            self.nbr_views = 0
        else:
            self.nbr_views+=1

    def __repr__(self):
        return f'Post id: {self.post_id} was viewed {self.nbr_views} times'
