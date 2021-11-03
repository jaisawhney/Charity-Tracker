from flask import Flask

app = Flask(__name__)


# Routes
@app.route("/")
def playlists_index():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
