import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_script import Manager, Server
from Flask_D01 import app
import flask_restful
from flask import Blueprint

manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000))
))
api = flask_restful.Api(app)

if __name__ == "__main__":
    manager.run()                                                                   