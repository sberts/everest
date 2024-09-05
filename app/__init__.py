from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import requests
import logging
from logging.handlers import RotatingFileHandler
import os
import boto3
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)

moment = Moment(app)

login = LoginManager(app)
login.login_view = 'login'

ses_client = boto3.client('ses',region_name=Config.AWS_REGION)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, errors

class DiscordWebhookHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record):
        try:
            log_entry = self.format(record)

            if len(log_entry) > 2000:
                log_entry = log_entry[:2000]

            payload = {
                "content": log_entry
            }
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(self.webhook_url, json=payload, headers=headers)
            if response.status_code != 204:
                print(f"Failed to send log to Discord: {response.text}")
        except Exception as e:
            print(f"Exception in DiscordWebhookHandler: {e}")
        # print(f'Sent log to Discord {log_entry}')

if app.config['DISCORD_WEBHOOK_URL']:
    discord_handler = DiscordWebhookHandler(app.config['DISCORD_WEBHOOK_URL'])
    discord_handler.setLevel(logging.ERROR)  # Change this to control the level of logging sent to Discord
    discord_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(discord_handler)

if app.config['LOG_TO_FILE']:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')
