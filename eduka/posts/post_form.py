## post_form.py inside the posts folder

from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField


class AddPostForm(FlaskForm):

    '''
    Form to add the posts.
    '''
    ## data required messages
    title_msg = 'Vous devez ajouter un titre à votre publication!'
    summary_msg = "Il est nécessaire d'ajouter un petit résumé!"

    post_title = StringField('titre:', validators=[DataRequired(message=title_msg)])
    post_summary = TextAreaField('résumé:',validators=[DataRequired(message=summary_msg)])
    start_date = DateField('date de commencement:')
    end_date = DateField('date de fin:')
    start_level = SelectField('mon niveau de commencement', choices=[('bg','débutant'), ('intr','intermédiaire'),
                                                                    ('adv','avancé'), ('exp', 'expert')],
                                                                    validators=[DataRequired()])

    end_level = SelectField('niveau envisagé à la fin:', choices=[('bg','débutant'), ('intr','intermédiaire'),
                                                                    ('adv','avancé'), ('exp', 'expert')],
                                                                    validators=[DataRequired()])


    post_category = StringField('ajouer le categorie:', validators=[DataRequired()])
    link1_title = StringField('ajouter un title pour le lien:')
    link1 = StringField('ajouter un lien:')

    link2_title = StringField('ajouter un title pour le lien:')
    link2 = StringField('ajouter un lien:')

    link3_title = StringField('ajouter un title pour le lien:')
    link3 = StringField('ajouter un lien:')

    link4_title = StringField('ajouter un title pour le lien:')
    link4 = StringField('ajouter un lien:')

    link5_title = StringField('ajouter un title pour le lien:')
    link5 = StringField('ajouter un lien:')

    submit = SubmitField('Ajouter')
