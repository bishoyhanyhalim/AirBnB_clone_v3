#!/usr/bin/python3
"""this is index file"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """return status to ok"""
    return jsonify({"status": "OK"})
