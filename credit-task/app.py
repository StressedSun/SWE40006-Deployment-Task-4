from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    greeting = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name:
            greeting = f"<h2>Hello, {escape(name)}!</h2>"

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

        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)