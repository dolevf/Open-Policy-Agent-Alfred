import sys
import os.path
import sqlite3
import config
import core.utils as utils

from flask import Flask, render_template, request, redirect
from flask import jsonify
from version import VERSION

app = Flask(__name__,  static_url_path='/static',  static_folder='static/',)

OPA_VERSION = utils.get_opa_version()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publish/<policyid>')
def published_view(policyid):
    policy = policyid.strip()
    con = sqlite3.connect(config.SQLITE3_DB_FILE_NAME)
    row = None
    data = {}
    with con:
        cur = con.cursor()
        cur.execute('SELECT id ,policy, data, input FROM policies WHERE id = ?', (policy,))
        row = cur.fetchone()

    if row:
        data['id'] = row[0]
        data['policy'] = row[1]
        data['data'] = row[2]
        data['input'] = row[3]

    return render_template('index.html', data=data)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    policy = request.json.get('policy', None)
    data = request.json.get('data', '') or ''
    inputs = request.json.get('inputs', None)
    coverage = request.json.get('coverage', False)

    result = []
    covered_lines = []
    non_covered_lines = []
    query_eval_ns = None

    policy_violation_name = utils.check_security_policy(policy)
    if policy_violation_name:
        result = ['{} is not allowed to be executed!'.format(policy_violation_name)]
    else:
        output = utils.opa_evaluate(policy, inputs, data, coverage)
        if 'result' in output:
            package_name = utils.get_package_name(policy)
            value = output['result'][0]['expressions'][0]['value']
            query_eval_ns = utils.get_query_eval_ns(output)
            covered_lines= utils.get_coverage(output, covered=True)
            non_covered_lines =  utils.get_coverage(output, covered=False)
            try:
                result = utils.get_recursively(value, package_name)[0]
            except IndexError:
                print('Error obtaining result.')

        elif 'errors' in output:
            for err in output['errors']:
                message = err['message']
                row = err['location']['row']
                code = err['code']
                result.append("{0}: {1}: {2} ".format(row, code, message))

    return jsonify({"result":result, "coverage":covered_lines, "no_coverage":non_covered_lines, "query_eval_ns":query_eval_ns})

@app.route('/publish', methods=['POST'])
def publish():
    policy = request.json.get('policy', None)
    data = request.json.get('data', '') or ''
    inputs = request.json.get('inputs', None)
    p_id = utils.generate_uuid()

    con = sqlite3.connect(config.SQLITE3_DB_FILE_NAME)

    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO policies (id, policy, data, input) VALUES (?,?,?,?)', (p_id, policy, data, inputs))

    return jsonify({"published_link":p_id})


@app.context_processor
def versions():
    return dict(opa_bin_version=OPA_VERSION, app_version=VERSION)

if __name__ == '__main__':
    if not os.path.exists('bin/opa'):
        print('Error: OPA Binary could not be found in/opa')
        sys.exit(1)
    if not os.path.exists(config.SQLITE3_DB_FILE_NAME):
        utils.create_db()
        
    app.run(port=5000, host='0.0.0.0', debug=False)
