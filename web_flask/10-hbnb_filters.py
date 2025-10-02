#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask
from flask import render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """view function that displays [...]"""
    all_states = storage.all("State").values()
    all_amenities = storage.all("Amenity").values()
    return render_template('10-hbnb_filters.html', all_states=all_states,
                           all_amenities=all_amenities)


@app.teardown_appcontext
def teardown(self):
    """function that removes the current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
