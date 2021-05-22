# -*- coding: utf-8 -*-
"""
Stack Overflow Tag predictor
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

from predict_tags import run_predictor

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

class NameForm(FlaskForm):
    field = TextAreaField('Your Question', validators=[DataRequired()], id='textfield')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm() 
    message = ''
    if form.validate_on_submit():
        question = form.field.data
        tags = run_predictor(question)
        message= 'Predicted Tags: ' + ', '.join(tags)
    return render_template('index.html', form=form, message=message)


if __name__ == "__main__":
    app.run()

