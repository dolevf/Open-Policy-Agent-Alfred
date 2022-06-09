import core.utils as utils

from flask import Flask, render_template, request
from flask import jsonify
from version import VERSION

app = Flask(__name__,  static_url_path='/static',  static_folder='static/',)

OPA_VERSION = utils.get_opa_version()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    policy = request.json.get('policy', None)
    data = request.json.get('data', '') or ''
    inputs = request.json.get('inputs', None)
    coverage = request.json.get('coverage', False)

    result = None
    covered_lines = []
    output = utils.opa_evaluate(policy, inputs, data, coverage)

    if 'result' in output:
        package_name = utils.get_package_name(policy)
        value = output['result'][0]['expressions'][0]['value']
        covered_lines = utils.get_coverage(output)
        result = utils.get_recursively(value, package_name)

    return jsonify({"result":result, "coverage":covered_lines})

@app.context_processor
def versions():
    return dict(opa_bin_version=OPA_VERSION, app_version=VERSION)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
