from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "hello",200

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8000)
    except Exception as e:
        pass
