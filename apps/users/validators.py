# from wtforms import Form, BooleanField, StringField, PasswordField, validators
# from flask import Flask, request, jsonify, Blueprint, session
# from apps.users.models import User
#
# class validateUsers(User):
#     username = StringField(User.name, [validators.length(min=4, max=25)])
#     email = StringField(User.email, [validators.Length(min=6, max=35),
#                                      validators.email_validator])
#     password = PasswordField(User.password, [validators.DataRequired(),
#         validators.length(min=5, max=120),
#     ])
