# MySql-Flask-Project
Flask Contact Form Project



# Flask Contact Form Project

This is a Flask-based web application that allows users to submit a contact form. The form collects basic information like the user's name, email, country, gender, subject, and message, and stores the data in a MySQL database. It also includes anti-spam measures (honeypot field) and basic form validation.

## Features

- Simple contact form with fields: First Name, Last Name, Email, Country, Gender, Subject, and Message.
- Form validation for required fields, gender, and email.
- Prevents spam submissions using a honeypot field.
- Data storage in a MySQL database.
- Flash messages for error handling and form submission success.
- Simple and clean design with HTML templates.

## Requirements

- Python 3.6+
- Flask
- MySQL Server (MySQL Workbench or another client for managing databases)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/flask-contact-form.git
    cd flask-contact-form
    ```

2. **Install dependencies**:
    Make sure you have `pip` installed and then install the required Python libraries:
    
    ```bash
    pip install Flask mysql-connector
    ```

3. **Setup MySQL Database**:
    - Create a MySQL database named `flask_project` in your MySQL instance.
    - Use the following commands to create the database and table:

    ```sql
    CREATE DATABASE flask_project;

    USE flask_project;

    CREATE TABLE IF NOT EXISTS contact_form( 
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL, 
        email VARCHAR(255) NOT NULL UNIQUE, 
        country VARCHAR(100) NOT NULL, 
        gender ENUM('Male', 'Female') NOT NULL,
        subject VARCHAR(255) NOT NULL,
        message TEXT NOT NULL
    );
    ```

4. **Configure MySQL Connection**:
    Update the MySQL credentials in the `app.py` file as per your local setup:
    ```python
    db = mysql.connector.connect(
        host="localhost",      # Change to your MySQL server
        user="root",           # Change to your MySQL username
        password="MySecure@123",  # Change to your MySQL password
        database="flask_project"  # Database name
    )
    ```

5. **Run the Flask Application**:
    Run the Flask app using the following command:
    ```bash
    python app.py
    ```

    This will start the server at `http://127.0.0.1:5000/` by default.

## Database Details

### Database: `flask_project`
This project uses a MySQL database named `flask_project` to store the submitted contact form data.

### Table: `contact_form`
The `contact_form` table stores information submitted via the contact form. The table structure is as follows:

| Column Name   | Data Type            | Description                                                                 | Constraints                |
| ------------- | -------------------- | --------------------------------------------------------------------------- | -------------------------- |
| `first_name`  | `VARCHAR(100)`        | Stores the user's first name.                                               | `NOT NULL`                 |
| `last_name`   | `VARCHAR(100)`        | Stores the user's last name.                                                | `NOT NULL`                 |
| `email`       | `VARCHAR(255)`        | Stores the user's email address.                                            | `NOT NULL`, `UNIQUE`       |
| `country`     | `VARCHAR(100)`        | Stores the user's country of origin.                                        | `NOT NULL`                 |
| `gender`      | `ENUM('Male', 'Female')` | Stores the user's gender.                                                  | `NOT NULL`                 |
| `subject`     | `VARCHAR(255)`        | Stores the subject selected by the user. Multiple subjects are stored as a comma-separated string. | `NOT NULL`                 |
| `message`     | `TEXT`                | Stores the user's message.                                                  | `NOT NULL`                 |

### Sample SQL for Table Creation:

```sql
CREATE TABLE IF NOT EXISTS contact_form( 
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL, 
    email VARCHAR(255) NOT NULL UNIQUE, 
    country VARCHAR(100) NOT NULL, 
    gender ENUM('Male', 'Female') NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL
);
```

## Flask Routes

### `/` (GET)
- Displays the contact form to the user.

### `/submit` (POST)
- Receives and processes the form submission.
- Validates the input fields and stores the data in the MySQL database.
- Displays a confirmation message upon successful submission or error if the data is invalid.

### `/home`
- A simple home route that logs an entry when accessed.

## Form Validation

1. **Gender Validation**: Ensures that the gender is either 'Male' or 'Female'.
2. **Email Validation**: Ensures that the email contains "@" and "." to validate its format.
3. **Spam Prevention**: Uses a honeypot field to detect and prevent automated spam submissions.
4. **Sanitization**: Removes HTML tags from the input fields to prevent XSS attacks.

## Flash Messages
The app uses Flask's `flash` method to display messages when validation fails or succeeds. These messages are displayed on the frontend after the form is submitted.

## Code Explanation

### Main Flask App (app.py)

- **Sanitization and Validation Functions**: `sanitize_input` cleans input strings by removing any HTML tags, and `validate_email` checks the email format.
- **Form Submission**: The form data is collected via `request.form`, and the SQL query is executed using `cursor.execute()`. The form is validated before submission.
- **MySQL Interaction**: The application uses MySQL’s `mysql-connector` Python library to connect and interact with the database. Data is inserted into the `contact_form` table using a prepared statement to prevent SQL injection.

### Templates (HTML Files)

- **`index.html`**: The form template where users input their information.
- **`thank_you.html`**: The page displayed after a successful form submission. It shows a confirmation message with the user's name.

## Troubleshooting

1. **Database Connection Issues**:
   - Ensure that the MySQL server is running.
   - Double-check the credentials (`host`, `user`, `password`, `database`) in the `app.py` file.
   
2. **Error Handling**:
   - If the form submission fails, check the server logs for detailed error messages.
   - Ensure that your table schema matches the one mentioned above.




