import json
import flask
from flask import request, jsonify
import base64

import candidates_viz_core as cvc

app = flask.Flask(__name__)
app.config["DEBUG"] = True

username = 'kevin_bi_bukitvista',
list_checklist_name_to_compare = ['Career Stage', 'Vital Attributes V2', 'Culture/Leadership Screening'] ,
board_name = 'TESTING PROJECT',
list_name = 'TEST KANDIDAT',  
candidate_names = ['KANDIDAT 1', 'KANDIDAT 2'],

@app.route('/api/v1/resources/candidates/viz/', methods=['GET'])
def candidates_viz():
    args_to_get = [
        'username',
        'api_key',
        'api_token',
        'list_checklist_name_to_compare',
        'board_name',
        'list_name',
        'candidate_names'
    ]

    user_args = dict()

    json_body = request.json

    print(json_body)
    keys = list(json_body.keys())

    for arg in args_to_get:
        if arg in keys:
            user_args[arg] = json_body[arg]
    
    if not (user_args['api_key'] is None):
        cvc.api_key = user_args['api_key']

    if not (user_args['api_token'] is None):
        cvc.api_key = user_args['api_token']

    viz_full_path = cvc.get_viz(
        user_args['username'],
        user_args['list_checklist_name_to_compare'],
        user_args['board_name'],
        user_args['list_name'],
        user_args['candidate_names']
    )

    with open(viz_full_path, 'rb') as viz_file:
        viz_base64 = base64.b64encode(viz_file.read()).decode('utf-8')

    return jsonify({'success': True, 'viz_png_base64': viz_base64})

app.run(port=8080)