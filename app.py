from flask import Flask

# create an instance of Flask
app = Flask(__name__) # __name__ is the name of the current module

@app.route('/')
def hello_world():
    return 'Hello, World!'