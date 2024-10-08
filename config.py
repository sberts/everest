import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL') or False
    LOG_TO_FILE = os.environ.get('LOG_TO_FILE') or False
    PROJECTS_PER_PAGE = 3
    AWS_REGION = os.environ.get('AWS_REGION') or 'us-west-2'
    NOREPLY_EMAIL = os.environ.get('NOREPLY_EMAIL') or 'Neatshell Password <no-reply@neatshell.com>'
    LANGUAGES = ['en', 'es']