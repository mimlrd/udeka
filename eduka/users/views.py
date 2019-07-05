## views.py inside users folder


from flask import (Blueprint, render_template, url_for,
                   flash, redirect, request, abort)
from eduka import login_manager, db
from eduka.users.user_forms import LoginForm, RegistrationForm, ForgotAccountForm, EditProfileForm
from flask_login import logout_user, login_required, login_user, current_user
from eduka.models import User, Post
from eduka.utils.other_utils import populate_edit_form
from werkzeug.utils import secure_filename

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    ## CHECK IF USER IS ALREADY LOGIN
    if current_user.is_authenticated:
		## we will need to change the link to logout
        return redirect(url_for('core.home'))

    if form.validate_on_submit():
        email = form.email.data
        pwd = form.password.data

        ## To log the user, need:
        ## 1 - check the user exist (is not none)
        ## 2 - check password math
        ## 3 - log user in

        ## 1 - check the user exist (is not none)
        usr = User.query.filter_by(email=email).first()

        ## 2 - check password math
        if usr.check_password(pwd) and usr is not None:
            login_user(usr)

        ## here we will add the next -- to forward the user
        ## to the intended page
            next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
            '''
            if not is_safe_url(next):
                return abort(400)

            '''

            return redirect(url_for('users.my_account', user_id=usr.id))

        else:
            flash(" The user doen't exist or the credentials are not correct, please try again!", 'danger')

    return render_template('login.html', form=form, title='Login page')



@users_blueprint.route('/registration', methods=['GET', 'POST'])
def registration():

    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        pwd = form.password.data

        ## save the data in the database
        new_usr = User(email=email, username=username, pwd=pwd)
        db.session.add(new_usr)
        db.session.commit()

        return redirect(url_for('users.login'))

    return render_template('registration.html', form=form, title='Regsitration page')



@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been log out!", 'warning')
    return redirect(url_for('users.login'))


######################################################
##													##
##               ACCOUNT PAGE       				##
##													##
######################################################


@users_blueprint.route('/<int:user_id>/account', methods=['GET', 'POST'])
@login_required
def my_account(user_id):

    title = "Ma page de profile"
    edit_form = EditProfileForm()
    ## The current_user is automatically passsed to the jinja template
    ## we need to to get the current_user Posts

    user = User.query.get_or_404(user_id)
    ## get all posts for the user in a descending order
    ## we could do it in one line, but prefer multiple
    ## lines to minimise mistakes
    p = Post.query.filter_by(user_id=user_id)
    p_desc = p.order_by(Post.date_posted.desc())
    posts = p_desc.all()

    ##### edit user ######
    populate_edit_form(user=user, form=edit_form)

    if edit_form.validate_on_submit():
        ## the form is okay, so we can save to the database
        new_email = request.form['email']
        new_bio = request.form['bio']
        print(f'new email: {new_email}, new bio: {new_bio}')




    return render_template('account.html', user=user,
                           user_id=user.id,
                           posts=posts,title=title,
                           form = edit_form)





######################################################
##													##
##               FORGOT PASSWORD      				##
##													##
######################################################


@users_blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot_pwd():

	form = ForgotAccountForm()

	if form.validate_on_submit():
		## send an email with a reset link to the user

		email_provided = form.email.data

		## 1- Check to see if email is in database
		## 2- Send email with reset link to user registered email address

		print(f'Info: {form.email.data}')

		return redirect(url_for('users.login'))

	return render_template('forgot_pwd.html', form=form, legend='Forgot Password')
