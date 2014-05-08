from functools import wraps
from flask import request
from app import apikey

def apikey_req(f):
    @wraps(f)
    def dec_func(*args, **kwargs):
        if request.form.get("apikey") == apikey:
            return f(*args, **kwargs)
        return "Key not valid."
    return dec_func