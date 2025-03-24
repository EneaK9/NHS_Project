from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running successfully on Railway!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
