from flask import Flask
from models import db, User, Car, Rental
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config_Config')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

