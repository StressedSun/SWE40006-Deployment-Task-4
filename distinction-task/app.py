from flask import Flask, request
from markupsafe import escape
import os

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "development")
GREETING_PREFIX = os.getenv("GREETING_PREFIX", "Hello")


@app.route("/", methods=["GET", "POST"])
def home():
    greeting = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name:
            greeting = f"<h2>{escape(GREETING_PREFIX)}, {escape(name)}!</h2>"

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Docker Flask App</title>
        </head>

        <body>
            <h1>What's your name?</h1>

            <form method="POST">
                <input
                    type="text"
                    name="name"
                    placeholder="Enter your name"
                    required
                >

                <button type="submit">Say Hello</button>
            </form>

            {greeting}

            <hr>
            <p>Environment: {escape(APP_ENV)}</p>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)