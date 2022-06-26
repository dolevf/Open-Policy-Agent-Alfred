import os
import json
import tempfile
import config
import uuid

tempfile.tempdir = "./temp"

def generate_uuid():
    return str(uuid.uuid4()).replace('-','')[0:8]

def run_cmd(cmd):
    return os.popen(cmd).read()

def check_security_policy(policy):
    allowed = False
    for line in policy.splitlines():
        if not line.startswith('#'):
            for key in config.RESTRICTED_BUILTINS:
                if key in line.strip():
                    allowed = key
    return allowed

def get_recursively(search_dict, field):
    fields_found = []

    for key, value in search_dict.items():
        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found

def get_coverage(result, covered=True):
    coverage = []
    key = 'covered'

    if not covered:
        key = 'not_covered'

    files = result.get('coverage', {}).get('files', [])
    for f in files:
        if key in files[f]:
            for i in files[f][key]:
                start = i['start']['row']
                end = i['end']['row']
                coverage.append({"start":start, "end":end})

    return coverage

def get_query_eval_ns(result):
    return result.get('metrics', {}).get('timer_rego_query_eval_ns', None)

def get_package_name(text):
    key_name = None
    for line in text.splitlines():
        if line.startswith('#'):
            continue

        if line.startswith('package'):
            package_name = line.split('package ')[-1]
            key_name = package_name.split('.')[-1]
            break

    return key_name

def get_opa_version():
    if os.path.exists('bin/opa'):
        return run_cmd("./bin/opa version | head -1 | awk -F'Version: ' '{print $2}'")
    return None

def write_file(data, filename):
    f = open(filename, "w")
    f.write(data)
    f.close()

def opa_evaluate(policy, inputs, data=' ', coverage=False):
    args = ''

    if coverage:
        args ='--coverage'

    policy_file = tempfile.NamedTemporaryFile(prefix='policy-', suffix='.rego').name
    input_file = tempfile.NamedTemporaryFile(prefix='input-', suffix='.text').name
    data_file = tempfile.NamedTemporaryFile(prefix='data-', suffix='.text').name

    write_file(policy, policy_file)
    write_file(inputs, input_file)
    write_file(data, data_file)

    res = None

    if data:
        res = run_cmd(f"./bin/opa eval -d {data_file} -i {input_file} -d {policy_file} --profile data {args}")
    else:
        res = run_cmd(f"./bin/opa eval -i {input_file} -d {policy_file} --profile data {args}")

    try:
        res = json.loads(res)
    except json.decoder.JSONDecodeError:
        return None

    for temp_file in policy_file, data_file, input_file:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return res