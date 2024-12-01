import requests
from flask import Flask, render_template, jsonify, session
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (this can also be in Redis, database, etc.)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize session
Session(app)

# Function to get a random cat fact from the API
def get_cat_fact():
    response = requests.get("https://catfact.ninja/fact")
    if response.status_code == 200:
        return response.json()['fact']
    return "No fact available at the moment."

@app.route("/")
def home():
    return render_template("index.html", show_cat_fact=False)

@app.route("/about")
def about():
    cat_fact = session.get('cat_fact', None)  # Get cat fact from session
    return render_template("about.html", cat_fact=cat_fact, show_cat_fact=True)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    cat_fact = session.get('cat_fact', None)  # Get cat fact from session
    return render_template("submit.html", cat_fact=cat_fact, show_cat_fact=True)

# Route to fetch a new cat fact and update session
@app.route("/update-cat-fact")
def update_cat_fact():
    cat_fact = get_cat_fact()  # Fetch a new cat fact
    session['cat_fact'] = cat_fact  # Store it in the session
    return jsonify({'cat_fact': cat_fact})  # Return the new cat fact as JSON

if __name__ == "__main__":
    app.run(debug=True)