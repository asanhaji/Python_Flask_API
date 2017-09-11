from flask import (Flask, flash, redirect, render_template, request, session, url_for, Blueprint, jsonify)
from Flask_D01 import app

mod_default = Blueprint('default', __name__)

@app.errorhandler(404)
def not_found(error):
    url = request.base_url
    if 'api' in url:
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    return render_template("404.html")

@app.errorhandler(405)
def method_not_found(error):
    url = request.url
    if 'api' in url:
        message = {
            'status': 405,
            'message': 'Method not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 405
        return resp
    return render_template("404.html")

@app.errorhandler(500)
def missing_argument(error):
    url = request.url
    if 'api' in url:
        message = {
            'status': 405,
            'message': 'Missing required argument: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp
    return render_template("404.html")

@mod_default.route('/')
@mod_default.route('/index')
def index():
    return render_template("index.html", current_page = "home")