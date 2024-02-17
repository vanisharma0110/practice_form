import random
import string
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template

# MySQL database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)
db_cursor = db_connection.cursor()

# Flask app initialization
app = Flask(__name__)

# Generate OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=4))

# Store OTP in database and send email
def process_form_data(name, email):
    otp = generate_otp()
    db_cursor.execute("INSERT INTO users (name, email, otp) VALUES (%s, %s, %s)", (name, email, otp))
    db_connection.commit()

    # Send email
    sender_email = "vanisharma132001@gmail.com"
    sender_password = "password"
    subject = "Your OTP"
    message = f"Hello {name},\nYour OTP is: {otp}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.vani.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, email, msg.as_string())
    server.quit()

# Define route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        process_form_data(name, email)
        return "OTP has been sent to your email. Please check."
    return render_template('index.html')

if __name__ == '__main__':
    # Create users table if not exists
    db_cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), otp VARCHAR(4))")
    app.run(debug=True)
