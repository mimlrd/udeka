## models.py


from eduka import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime as dt

##load the current user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    '''
    User class that will determine ...
    '''
    default_bio = "Utilisateur n'a pas encore ajouter un bio "
    default_profile_link = "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image_link = db.Column(db.String(350), nullable=True,
                                    default=default_profile_link)
    email = db.Column(db.String(80), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    bio = db.Column(db.Text(200), default=default_bio)
    hash_password = db.Column(db.String(256))
    # This connects Posts to a User Author.
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, email, username, pwd, bio=None, profile_image_link=None):
        self.email = email
        self.username = username
        self.bio = bio
        self.profile_image_link = profile_image_link
        self.hash_password = generate_password_hash(pwd)

    def __repr__(self):
        return f'Username: {self.username} and email: {self.email}'

    def check_password(self, pwd):
        return check_password_hash(self.hash_password, pwd)


class Post(db.Model):

    # Setup the relationship to the User table
    users = db.relationship(User)

    '''
    Post class will determine how the user add a post.
    '''

    __tablename__ = 'posts'
    default_post_img_link = "https://cdn.pixabay.com/photo/2019/05/01/21/39/programming-4172154_960_720.jpg"

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, index=True, default=dt.utcnow)
    title = db.Column(db.String(200), unique=True, nullable=False)
    summary = db.Column(db.Text(), nullable=False)
    date_start = db.Column(db.DateTime, default=dt.utcnow)
    ## need to find a way to automatically add 7 days to starte date as default
    date_end = db.Column(db.DateTime, default=dt.utcnow)
    level_beg = db.Column(db.Integer, default=1)
    level_end = db.Column(db.Integer, default=1)

    ##---> Rename category - tags (might need to create own table Tag)
    ##---> tags need to be indexed, so users could search (query) easily by tag
    category = db.Column(db.String(), default='IT')
    post_image_link = db.Column(db.String(350), nullable=True,
                                default=default_post_img_link)
    ##nbr_views = db.Column(db.Integer, default=0)
    # Connect this table with other tables such as users and links
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    links = db.relationship('PostLink', backref='post_link', lazy=True)
    nbr_views = db.relationship('PostView', backref='post_view', lazy=True)

    def __init__(self, title, summary,
                 level_beg,
                 level_end, category, user_id, date_end, date_start=None):

        self.title = title;
        self.summary = summary;
        self.date_start = date_start;
        self.date_end = date_end;
        self.level_beg = level_beg;
        self.level_end = level_end;
        self.category = category;
        self.user_id = user_id
        ##self.date_posted = dt.utcnow

    def __repr__(self):
        return f'Post title: {self.title} and started at level:{self.level_beg}'




class PostLink(db.Model):
    '''
    The post links here.
    '''

    # Setup the relationship to the User table
    posts = db.relationship(Post)

    __tablename__ = 'postlinks'

    id = db.Column(db.Integer, primary_key=True)
    link_title = db.Column(db.String(200), nullable=False)
    link_url = db.Column(db.String(), unique=True, nullable=False)
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
