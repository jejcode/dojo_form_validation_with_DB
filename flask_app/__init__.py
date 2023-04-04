from flask import Flask # import flask to create an instance for app
app = Flask(__name__) # create instance of Flask
app.secret_key = "I finally get to use my secret key!"