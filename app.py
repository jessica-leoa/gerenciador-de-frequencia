from extensions import db
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    @app.route("/")
    def hello():
        return "Hello World from Flask + Docker!"

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)



  
