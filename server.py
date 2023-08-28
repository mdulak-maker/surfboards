from flask_app import app
from flask_app.controllers import users, surfboards
if __name__ == "__main__":
    app.run(debug=True)