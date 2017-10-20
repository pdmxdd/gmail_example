from flask import Flask, render_template, flash, request

from emailer import send_email

app = Flask(__name__)
app.config['DEBUG'] = True
# super_secret_string is an awful secret key, but works fine for this example, you'd ideally create a 32 long random string
app.config['SECRET_KEY'] = "super_secret_string"



@app.route('/home')
def home():
    name = 'Paul'
    return "<h1>Welcome to the home page {}!<h1>".format(name)

@app.route('/email', methods=['GET'])
def email():
    return render_template("email.html")

@app.route('/email', methods=['POST'])
def email_post():
    to = request.form['email_to']
    subject = request.form['email_subject']
    message = request.form['email_message']
    send_email(to, subject, message)
    flash("Email Sent Successfully")
    return render_template("email.html")



if __name__ == '__main__':
    app.run()