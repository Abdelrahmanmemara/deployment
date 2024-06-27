import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__, 
            template_folder='./templates', 
            static_folder='./static')
app.secret_key = 'supersecretkey'  # Needed for flash messages

USER_DATA_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    """
    Load users from JSON file.
    Returns: Dictionary with user data.
    """
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    """
    Save users in JSON file.
    """
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

users = load_users()

def is_valid_password(password):
    """
    Validate password based on criteria:
    - At least 8 characters long
    - Contains at least 1 capital letter
    - Contains at least 1 number or special symbol
    Returns: True if valid, False otherwise.
    """
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() or not char.isalnum() for char in password):
        return False
    return True

@app.route('/images/<path:filename>')
def serve_images(filename):
    """
    Serve images from the images folder.
    """
    return send_from_directory('./static/images', filename)

@app.route('/')
def index():
    """
    Render the index.html template.
    Returns: Rendered index template.
    """
    return render_template('index.html')

@app.route('/index1')
def index1():
    """
    Render the index1.html template.
    Returns: Rendered index template for login.
    """
    return render_template('index1.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    Returns:
        Response: Rendered HTML template of login page or redirect to index page.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['login-password']
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            flash("Login successful!", 'success')
            return redirect(url_for('profile', email=email))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """
    Handle user registration.

    Returns:
        Response: Rendered HTML template of sign up page or redirect to another index page.
    """
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['signup-password']
        verify_password = request.form['verify-password']

        if password != verify_password:
            flash('Passwords do not match!', 'danger')
        elif email in users:
            flash('Email already registered!', 'danger')
        elif not is_valid_password(password):
            flash('Password must be at least 8 characters long and contain at least 1 capital letter and 1 number or special symbol.', 'danger')
        else:
            users[email] = {
                'firstname': firstname,
                'lastname': lastname,
                'password': generate_password_hash(password)
            }
            save_users(users)  
            flash("Sign up successful!", 'success')
            return redirect(url_for('profile', email=email))
    return render_template('sign-up.html')

@app.route('/about-us')
def about_us():
    """
    Render the about-us.html template.
    Returns: About us page.
    """
    return render_template('about-us.html')

@app.route('/about-us1')
def about_us1():
    """
    Render the about-us.html template.
    Returns: About us page for login.
    """
    return render_template('about-us1.html')

@app.route('/error')
def error():
    """
    Render the error.html template.
    Returns: Error page.
    """
    return render_template('error.html')

@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 Not Found errors.

    Input: e (= Exception object)

    Returns: Rendered HTML template for the error page.
    """
    return render_template('error.html'), 404

@app.route('/search-mysterious-flights')
def search_mysterious_flights():
    """
    Render the search-mysterious-flights.html template.
    Returns: Search page for mysterious flights.
    """
    return render_template('search-mysterious-flights.html')

@app.route('/search-mysterious-flights1')
def search_mysterious_flights1():
    """
    Render the search-mysterious-flights1.html template.
    Returns: Search page for mysterious flights for login.
    """
    return render_template('search-mysterious-flights1.html')

@app.route('/search-normal-flights')
def search_normal_flights():
    """
    Render the search-normal-flights.html template.
    Returns: Search page for normal (non-mysterious) flights.
    """
    return render_template('search-normal-flights.html')

@app.route('/search-normal-flights1')
def search_normal_flights1():
    """
    Render the search-normal-flights1.html template .
    Returns: Search page for normal (non-mysterious) flights when you logged in.
    """
    return render_template('search-normal-flights1.html')

@app.route('/search-result-mysterious-flight')
def search_result_mysterious_flight():
    """
    Render the search-result-mysterious-flight.html template.
    Returns: Search results for mysterious flights.
    """
    return render_template('search-result-mysterious-flight.html')

@app.route('/search-result-mysterious-flight1')
def search_result_mysterious_flight1():
    """
    Render the search-result-mysterious-flight1.html template.
    Returns: Search results for mysterious flights for login.
    """
    return render_template('search-result-mysterious-flight1.html')

@app.route('/search-result-normal-flight')
def search_result_normal_flight():
    """
    Render the search-result-normal-flight.html template.
    Returns: Search results for normal (non-mysterious) flights.
    """
    return render_template('search-result-normal-flight.html')

@app.route('/search-result-normal-flight1')
def search_result_normal_flight1():
    """
    Render the search-result-normal-flight1.html template.
    Returns: Search results for normal (non-mysterious) flights for login.
    """
    return render_template('search-result-normal-flight1.html')


@app.route('/profile')
def profile():
    """
    Render the profile.html template with the user's information.
    Returns: Rendered profile page.
    """
    email = request.args.get('email')
    user = users.get(email)
    if user:
        return render_template('profile.html', user=user)
    else:
        flash('User not found!', 'danger')
        return redirect(url_for('index'))



@app.route('/update_email', methods=['POST'])
def update_email():
    current_email = request.form['current-email']
    new_email = request.form['new-email']
    if current_email in users:
        users[new_email] = users.pop(current_email)
        save_users(users)
        flash('Email updated successfully!', 'success')
    else:
        flash('Current email not found!', 'danger')
    return redirect(url_for('profile'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    email = request.form['delete-email']
    password = request.form['delete-password']
    user = users.get(email)
    if user and check_password_hash(user['password'], password):
        users.pop(email)
        flash('Account deleted successfully!', 'danger')
    else:
        flash('Invalid email or password!', 'danger')
        return redirect(url_for('profile'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
