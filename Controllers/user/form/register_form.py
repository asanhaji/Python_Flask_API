from wtforms import Form, BooleanField, TextField, PasswordField, validators 
class RegisterForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20), validators.Regexp('^[a-zA-Z0-9_.-]*$', message="Usename must contain only letters un numbers or underscore")])
    email = TextField('Email Address', [validators.Length(min=6, max=50), validators.Email()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=4, max=20)
    ])
    confirm = PasswordField('Repeat Password')