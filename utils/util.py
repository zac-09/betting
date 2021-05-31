from flask import Flask,jsonify, abort, make_response,request
from functools import wraps
import os
def api_key_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        # key = os.environ.get("API_KEY")
        key = "1254"
        print("the key is",key)
        print("from headers",request.headers.get('api-key'))
        if  request.headers.get('api-key') == key:
            return function(*args, **kwargs)
        else:
            abort(make_response(jsonify(message="please contanct admin for api key"), 403))
    return decorated_function