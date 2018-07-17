import json
def check_request_update(request_info, username, access_token):
    output_filename = request_info['output_filename']
    request_url = request_info['request_url']

    request_info['access_token'] = access_token
    request_info['server_address'] = beta_server
    request_url = '%(server_address)s/v1/layers/task/?access_token=%(access_token)s&task_id=%(task_id)s' % request_info
    r = requests.get(request_url)
    print r.content

    request_info = json.loads(r.content)
    request_info['output_filename'] = output_filename
    request_info['request_url'] = request_url

    return request_info

def print_task_list(access_token):
    request_info = {}
    request_info['server_address'] = beta_server
    request_info['access_token'] = access_token
    request_url = '%(server_address)s/v1/layers/task_list/?access_token=%(access_token)s' % request_info
    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    # print response_body
    task_list = json.loads(response_body)

    for task in task_list:
        print task