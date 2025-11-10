from flask import Flask
import os

app = Flask(__name__)

app.config["DEBUG"] = os.getenv("DEBUG", "False") == "True"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret")

@app.route("/")
def home():
    mode = "Debug" if app.config["DEBUG"] else "Production"
    return f"App running in {mode} mode."

if __name__ == "__main__":
    app.run()