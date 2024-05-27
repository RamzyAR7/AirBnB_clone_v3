#!/usr/bin/python3
""" script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """displays Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """displays HBNB"""
    return "HBNB"


@app.route("/c/<text>")
def c(text):
    """displays C followed by the value of the text"""
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """displays Python followed by the value of the text"""
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route("/number/<int:n>", strict_slashes=False)
def num(n):
    """display "n is a number" only if n is an integer"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def num_temp(n):
    """display a HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def num_odd_or_even(n):
    """display a HTML page only if n is an integer"""
    return render_template('6-number_odd_or_even.html', n=n)


@app.route('/states', strict_slashes=False)
@app.route('/states_list', strict_slashes=False)
def states_list():
    """display a HTML page with states list"""
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page cities_by_states"""
    states = storage.all("State")
    cities = storage.all("City")
    return render_template('8-cities_by_states.html', states=states,
                           cities=cities)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id=None):
    """Display a HTML page with state and cities_by_states"""
    target_state = None
    states = storage.all("State")
    cities = storage.all("City")
    for state in states.values():
        if state.id == id:
            target_state = state
    return render_template('9-states.html', cities=cities,
                           state=target_state)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display a HTML page hbnb_filters"""
    states = storage.all("State")
    cities = storage.all("City")
    amenities = storage.all("Amenity")
    return render_template('10-hbnb_filters.html', states=states,
                           cities=cities, amenities=amenities)


@app.teardown_appcontext
def teardown_appcontext(*args):
    """After each request remove current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
