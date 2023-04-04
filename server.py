from flask_app import app
from flask_app.controllers import users # import controller to run routes
    
if __name__ == '__main__': # make sure app is running directly and not from a different module
    app.run(debug = True, port = 8000) # run app in debug mode on port 8000