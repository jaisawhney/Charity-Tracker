from flask import Flask
import os

app = Flask(__name__)


# Routes
@app.route("/")
def playlists_index():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
