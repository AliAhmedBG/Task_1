class Config:
    SECRET_KEY = 'devkey123'
    DEBUG = True
    TESTING = True
    # tells Flask-WTF to enable CSRF protection for forms
    WTF_CSRF_ENABLED = True