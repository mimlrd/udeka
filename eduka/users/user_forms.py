## user_forms.py in users folder

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from eduka.models import User ## To check the curent user


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe')
    remember = BooleanField('Se souvenir de moi', default="checked")
    submit = SubmitField('Connexion')




class RegistrationForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[Length(min=8)])
    re_password = PasswordField('Retaper nom de passe',
                              validators=[EqualTo(fieldname='password',
                                                  message='Mot de passe doit être pareil!')])
    submit = SubmitField("M'inscrire")

    ############################ CUSTOM VALIDATORS ################################################

	## to validate the field before submit is done - so can check for uniquenesss of some data
	## the following is a template for our validation
	## we want to check if the username already exist in our database
    def validate_username(self, username):
		## we are going to query the database to see if the user already exist
		## we will do the checks only if the new data provided is different from the one in the database
        user = User.query.filter_by(username=username.data).first()
        if user:
            ## if user exist already, then send a validation error
            raise ValidationError('This username is already taken. Please choose another username.')


	## we want to check if the email already exist in our database
    def validate_email(self, email):
        ## we are going to query the database to see if the user already exist
        user = User.query.filter_by(email=email.data).first()
        if user:
            ## if user exist already, then send a validation error
            raise ValidationError('This email is already in used. Please choose another email.')

	############################ CUSTOM VALIDATORS ################################################




class ForgotAccountForm(FlaskForm):

	#### form to fill if forgot account

	email = StringField('Adresse Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Récuperer')
