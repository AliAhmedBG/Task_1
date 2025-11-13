#imports libraries
from flask_wtf import *
from wtforms import *
from wtforms.validators import *

# contains a set of usernames that arent allowed to be used by the user
reservedUsernames = {"admin", "root", "superuser"}
#only emails ending in one of these is allowed
validEmailSuffix = (".edu", ".ac.uk", ".org")

# This variable contains common passwords which the user will not be allowed to use
commonPasswords = {"password123",
"admin",
"123456",
"qwerty",
"letmein",
"welcome",
"iloveyou",
"abc123",
"monkey",
"football"}

# This class initiations are registration form for the user to enter their details which will be checked
class RegistrationForm(FlaskForm):
    """ This sets the username field which checks for the following:
    - the username field must be filled in
    - has to be between 3 and 30 characters
    - the only things allowed are letters and underscores"""
    username = StringField("Username", validators=[DataRequired(message = "Please enter a valid username"),
                                                   Length(min = 3, max = 30, message = "Username can only be between 3 and 30 characters"),
                                                   Regexp(r"^[A-Za-z_]+$", message="Username can only contain letters and underscores."),])


    # Creates a required email field which must pass the wtforms email check
    email = StringField("Email", validators = [DataRequired(message = "Email required"),
                                               Email(message = "Please enter a valid email address"),])

    # Creates a password field which must be filled and has to be atleast 12 characters, further checks are done below
    password = PasswordField("Password", validators = [DataRequired(message = "Password required"),
                                                       Length(min = 12, message = "Password must be atleast 12 characters"),])

    # creates a second field for the password where the input must match the input for the first password field
    confirmPassword = PasswordField("Confirm Password", validators = [DataRequired(message = "Please confirm your password"),
                                                                      EqualTo("password", message = "Passwords must match"),])

    # Bio field for the user to enter text, can use tags to alter whats entered but thats handled later on
    bio = TextAreaField("Bio", validators = [DataRequired(message = "Please enter your bio"),])

    # Submit button
    submit = SubmitField("Register")

    def validate_username(self, field):
        # checks if the lowercase version of usename and the normal version is in the reservedUsername list
        if field.data and field.data.lower() in reservedUsernames:
            # if it exists this validation error is raised which tells the user what happened so they can fix it
            raise ValidationError("This username is not allowed. Please pick another one")

    def validate_email(self, field):
        # Checks that the email ends with the allowed endings
        if not field.data.strip().lower().endswith(validEmailSuffix):
            # if it ends with something else then this validation error is raised
            raise ValidationError("This email is not allowed. Please pick another one")

    # This function enforces the password policies
    def validate_password(self, field):
        password = field.data
        # Makes checks against the lowercase version of username and email as its simpler
        username = self.username.data.lower()
        email = self.email.data.lower()

        # Checks that there is atleast one upper case characters and raises the appropriate error if not
        hasUpper = any(char.isupper() for char in password)
        if hasUpper is False:
            raise ValidationError("Password must include at least one uppercase letter")

        # does the same check but for lowercase characters
        hasLower = any(char.islower() for char in password)
        if hasLower is False:
            raise ValidationError("Password must include at least one lowercase letter")

        # Checks that there is atleast one digit eg 1 or 4 and raises the appropriate error message if not
        hasDigit = any(char.isdigit() for char in password)
        if hasDigit is False:
            raise ValidationError("Password must contain at least one digit")

        # Checks that there is atleast 1 special character eg "!"
        hasSpecial = any(not char.isalnum() for char in password)
        if hasSpecial is False:
            raise ValidationError("Password must include at least one special character")

        # Ensures that there is no whitespace and raises an error if there is any
        hasWhitespace = any(char.isspace() for char in password)
        if hasWhitespace:
            raise ValidationError("Password cannot include whitespace")

        # Checks if the lowercase version of the password is a common password and raises an error if it is
        if password.lower() in commonPasswords:
            raise ValidationError("Password is too common, please choose another password")

        # Final check to see if the username or email is anywhere in the password and raises an error if it is
        if username in password.lower() or email in password.lower():
            raise ValidationError("password cannot contain username or email")
