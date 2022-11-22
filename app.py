from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return None


if __name__ == '__main__':
    app.run()
