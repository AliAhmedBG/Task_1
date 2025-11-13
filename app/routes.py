from flask import *
import logging
from .forms import *
import bleach

main = Blueprint('main', __name__)

# Lists the html tags allowed in the bio field
allowedTags = ["b", "i", "u", "em", "strong",
    "a", "p", "ul", "ol", "li"]

# Allows attributes on specific tags which are only href and title on <a>.
allowedAttributes = {"a": ["href", "title"]}

#CHANGE ----------------------------------------------------------
def getClientIP():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"
#CHANGE ----------------------------------------------------------



@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    sanitisedBio = None
    clientIP = getClientIP()

    if form.validate_on_submit():
        rawBio = form.bio.data

        sanitisedBio = bleach.clean(rawBio, tags = allowedTags, attributes = allowedAttributes, strip = True)

        if sanitisedBio != rawBio:
            current_app.logger.warning(
                "Bio contains invalid HTML tags. IP=%s username=%s", clientIP, form.username.data,)

        current_app.logger.info(
            "registration complete. IP=%s username=%s email=%s",clientIP, form.username.data, form.email.data)

        flash("Registration complete (Account creation simulated.)", "success")
        return render_template("register.html", form=form, bio=sanitisedBio)

    elif request.method == 'POST':
        current_app.logger.warning("Validation failed. IP=%s errors=%s", clientIP, dict(form.errors))
        flash("There were problems with your registration. here are the errors below.", "error")

    return render_template("register.html", form=form, bio=sanitisedBio)


