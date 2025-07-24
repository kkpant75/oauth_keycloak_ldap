from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, HTTPS World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context=("certs/cert.pem", "certs/key.pem"),debug=True)
    #app.run(host="0.0.0.0", port=5000,debug=True)