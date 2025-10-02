#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask
from flask import render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_id(id=None):
    """view function that displays the state/cities objects with a given id"""
    all_states = storage.all("State").values()
    state_found = None
    if id is not None:
        for state in all_states:
            if state.id == id:
                state_found = state
    return render_template('9-states.html', all_states=all_states, id=id,
                           state_found=state_found)


@app.teardown_appcontext
def teardown(self):
    """function that removes the current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
