from flask import Flask, jsonify, request
from models.grouper import Grouper

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    gpr = Grouper()
    print(f"app: root: gpr.get_groups(): {gpr.get_groups()}")
    return ''


@app.route('/grouper', methods=['POST'])
def grouper():
    req_data = request.json
    gpr = Grouper(req_data)
    combo_groups = gpr.get_groups()
    res_data = {"combinations": combo_groups}
    return jsonify(res_data)


if __name__ == '__main__':
    app.run()
