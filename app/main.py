from flask import Flask

from app.routes.phone_tracker_routes import phone_blueprint

app = Flask(__name__)


app.register_blueprint(phone_blueprint, url_prefix="/")


if __name__ == '__main__':
    app.run(debug=True)