from flask import Flask, render_template
from flask import request, flash
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS"))

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get("EMAIL_USER"),
    "MAIL_PASSWORD": os.environ.get("EMAIL_PASSWORD"),
}

app.config.update(mail_settings)
mail = Mail(app)


@app.route("/contactform", methods=["POST"])
def contact_us():
    # Send email to admins
    email_body = f"{request.form['name']} filled contact us form for compilers.live \
    and here is the message: \n{request.form['message']}."
    msg = Message(
        subject=request.form["subject"],
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[app.config.get("MAIL_USERNAME")],
        body=email_body,
    )
    mail.send(msg)

    # Send acknowledment email to user
    email_body = f"Hi {request.form['name']}, \nThank you \
    for getting in touch with us. \
    We will review your message and get back to you. \
    \n\nRegards,\nCompiler.team"

    msg = Message(
        subject="[compilers.live] Thanks for enquiry",
        sender="contact@compilers.live",
        recipients=[request.form["email"]],
        body=email_body,
    )
    mail.send(msg)

    flash("Form submitted successfully!", "info")
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
