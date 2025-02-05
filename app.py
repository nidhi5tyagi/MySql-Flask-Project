from flask import Flask, render_template, request, redirect, url_for, flash
import re
import logging
import mysql.connector

# Function to sanitize input (remove HTML tags for XSS prevention)
def sanitize_input(input_string):
    return re.sub(r'<.*?>', '', input_string)  # Remove HTML tags from the input string

# Function to validate email format
def validate_email(email):
    if "@" not in email or "." not in email:
        return False
    return True

# Initialize the Flask application
app = Flask(__name__)

# Secret key for session management (needed for flash messages)
app.secret_key = 'my_super_secret_key_123'

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",      # Change to your MySQL server
    user="root",  # Change to your MySQL username
    password="MySecure@123",  # Change to your MySQL password
    database="flask_project"  # Change to your database name
)

# Create a cursor object to interact with the MySQL database
cursor = db.cursor()

# Create the contact_form table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_form( 
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL, 
        email VARCHAR(255) NOT NULL UNIQUE, 
        country VARCHAR(100) NOT NULL, 
        gender ENUM('Male', 'Female') NOT NULL,
        subject VARCHAR(255) NOT NULL,
        message TEXT NOT NULL
    )
""")

@app.route("/home")
def home():
    app.logger.info("Home route accessed")
    return "Welcome to Hackers Poulette™!"

@app.route("/", methods=["GET"])
def index():
    app.logger.info("Form accessed")
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Honeypot field to prevent spam
    honeypot = request.form.get("honeypot")

    # If the honeypot field is filled, treat it as a spam submission
    if honeypot:
        flash("Spam detected! Your form submission has been ignored.")
        return redirect(url_for('home'))  # Redirect back to the form

    # Get form data
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    country = request.form["country"]
    gender = request.form["gender"]
    subject = request.form.getlist("subject")
    message = request.form["message"]

    # Print form data (for debugging)
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Email: {email}")
    print(f"Country: {country}")
    print(f"Gender: {gender}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")

    # Handle the subject field correctly (single or multiple)
    subject_list = request.form.getlist("subject")  # This returns a list if multiple checkboxes are used
    subject = ', '.join(subject_list) if subject_list else sanitize_input(request.form["subject"])

    # Validate gender input (check if it's either 'Male' or 'Female')
    if gender not in ['Male', 'Female']:
        flash("Invalid gender value! Please select 'Male' or 'Female'.")
        return redirect(url_for('index'))

    # SQL query to insert data into the contact_form table
    query = "INSERT INTO contact_form (first_name, last_name, email, country, gender, subject, message) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (first_name, last_name, email, country, gender, subject, message)

    # Print the query and values (for debugging)
    print(f"Executing query: {query}")
    print(f"With values: {values}")

    # Execute the query and commit the changes to the database
    try:
        cursor.execute(query, values)
        db.commit()  # Save changes
        return f"User {first_name} {last_name} added successfully!"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return f"Error: {err}"

    # Render the thank you page after form submission
    return render_template("thank_you.html", first_name=first_name, last_name=last_name)

# Run the Flask application
if __name__ == "__main__":
    # Uncomment to run with a custom server (optional)
    # serve(app, host='0.0.0.0', port=8080)
    app.run(debug=True)
