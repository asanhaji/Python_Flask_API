from wtforms import Form, TextField, PasswordField, validators 
class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [
        validators.Required(),
    ])
