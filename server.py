from flask_app import app
from flask_app.controllers import users, surfboards

import boto3

import os

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    app.run(debug=True)