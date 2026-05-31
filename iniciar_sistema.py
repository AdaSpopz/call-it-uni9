from flask import Flask

app = Flask(__name__, template_folder="../views", static_folder="../static")

from api.rotas import app  

if __name__ == "__main__":
    app.run(debug=True)