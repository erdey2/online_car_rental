from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Setup Flask-Migrate
migrate = Migrate(app, db)

from app import routes  # Ensure your routes are imported

if __name__ == '__main__':
    app.run(debug=True)


