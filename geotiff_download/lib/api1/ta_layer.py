def get_all_layers_list(block_dic_struct, product_name,
                        username, access_token):
    if product_name in ('MULTIBAND', 'FULL'):
        product_name = 'NDVI'

    request_url = 'https://api.terravion.com/v1/users/' + username + \
        '/layers?product=' + product_name + '&access_token=' + access_token

    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    layer_list_json = json.loads(response_body)

    # Organize the layer_id with block_name
    layer_list = []

    for layer_info in layer_list_json:
        layer_struct = {}
        layer_struct['id'] = layer_info['id']
        layer_struct['layerdate'] = layer_info['layerDate']
        layer_struct['product'] = layer_info['product']
        layer_struct['block_id'] = layer_info['block']['id']
        layer_struct['block_name'] = block_dic_struct[layer_info['block']['id']]['block_name']
        layer_list.append(layer_struct)

    return layer_list
def get_layer_by_add_date(block_dic_struct, product_name, username,
                          access_token, addEpochStart, addEpochEnd):
    # addEpochStart=1457191383&addEpochEnd=1471047970&product=NC&access_token=849811e8-2fbe-4c3e-93e9-980b15a38426
    if product_name == 'MULTIBAND':
        product_name = 'NDVI'

    request_info = {}
    request_info['username'] = username
    request_info['product_name'] = product_name
    request_info['access_token'] = access_token
    request_info['addEpochStart'] = addEpochStart
    request_info['addEpochEnd'] = addEpochEnd
    request_url = 'https://api.terravion.com/v1/users/%(username)s/layers?addEpochStart=%(addEpochStart)s&addEpochEnd=%(addEpochEnd)s&product=%(product_name)s&access_token=%(access_token)s' % request_info
    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    layer_list_json = json.loads(response_body)
    # Organize the layer_id with block_name
    layer_list = []

    for layer_info in layer_list_json:
        layer_struct = {}
        layer_struct['id'] = layer_info['id']
        layer_struct['layerdate'] = layer_info['layerDate']
        layer_struct['product'] = layer_info['product']
        layer_struct['product_name'] = product_name
        layer_struct['block_id'] = layer_info['block']['id']
        layer_struct['block_name'] = block_dic_struct[layer_info['block']['id']]['block_name']
        layer_list.append(layer_struct)

    return layer_list

def make_download_request(output_filename, access_token, layer_id,
                          product_name, color_map=None, RGB_color_map=None):
    request_info = {}
    request_info['access_token'] = access_token
    request_info['server_address'] = beta_server
    request_info['layer_id'] = layer_id

    if product_name == 'MULTIBAND':
        request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/multiband.tiff?access_token=%(access_token)s' % request_info

    elif 'NC' == product_name or 'CIR' == product_name:
        request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=null&access_token=%(access_token)s' % request_info

    elif 'TIRS' == product_name:
        if RGB_color_map:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=T&access_token=%(access_token)s&isColormapRgb=true' % request_info
        else:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=T&access_token=%(access_token)s' % request_info

    elif 'NDVI' == product_name or 'ZONE' == product_name:
        request_info['colorMap'] = urllib.quote(color_map)

        if RGB_color_map:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=%(colorMap)s&access_token=%(access_token)s&isColormapRgb=true' % request_info
        else:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=%(colorMap)s&access_token=%(access_token)s' % request_info

    # print request_url
    # response_file = urlopen(request)

    try:
        print 'output_filename:', output_filename
        print 'request_url:', request_url
        r = requests.get(request_url)
        print r

        response_info = json.loads(r.content)
        response_info['output_filename'] = output_filename
        response_info['request_url'] = request_url
        time.sleep(1)

        return response_info

    except:
        if request_info:
            error_message = request_info
        else:
            error_message = {}

        error_message['request_url'] = request_url
        error_message['output_filename'] = output_filename
        error_message['status'] = 'ERROR'
        error_message['message'] = str(traceback.format_exc())

        print traceback.format_exc()

        return error_message

def get_layer_list(block_dic_struct):
    # Get the layer list of the users between the time period of start_date
    # and end_date and organize the layers by the block_name
    request_url = 'https://api.terravion.com/v1/users/' + \
        username + '/layers?epochStart=' + \
        str(start_date_epoc) + '&epochEnd=' + str(end_date_epoc) + \
        '&product=' + product_name + '&access_token=' + access_token

    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    layer_list_json = json.loads(response_body)

    # Organize the layer_id with block_name
    layer_list = []

    for layer_info in layer_list_json:
        print layer_info
        layer_struct = {}
        layer_struct['id'] = layer_info['id']
        layer_struct['layerdate'] = layer_info['layerDate']
        layer_struct['product'] = layer_info['product']
        layer_struct['block_id'] = layer_info['block']['id']
        layer_struct['block_name'] = block_dic_struct[layer_info['block']['id']]['block_name']
        layer_list.append(layer_struct)

    return layer_list