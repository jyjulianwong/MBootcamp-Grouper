from flask import Flask, jsonify, request
from flask_cors import CORS
from models.grouper import Grouper

application = Flask(__name__)
CORS(application)


@application.route('/', methods=['GET'])
def root():
    gpr = Grouper()
    print(f"app: root: gpr.get_groups(): {gpr.get_groups()}")
    return ''


@application.route('/grouper', methods=['POST'])
def grouper():
    req_data = request.json
    gpr = Grouper(req_data)
    combo_groups = gpr.get_groups()
    res_data = {"combinations": combo_groups}
    return jsonify(res_data)


if __name__ == '__main__':
    application.run()
