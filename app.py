import os
from flask import Flask
from views import routes

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
