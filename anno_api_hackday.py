#! /usr/bin/python3

from __future__ import print_function
import sys
from flask import Flask, jsonify, abort, make_response, request
import requests
import cloudant
import json
import jsonschema
from jsonschema import validate


app = Flask(__name__)

# Global configuration variables
# Access to variables as config['key'] and config['passphrase']
# api_url is the cloudant database url
# Register and create db @ cloudant.com
config = {
    "key":"peredgerdedediffeetheret",
    "passphrase":"292ce457c87db9ec202e9bd60ec833426dba271e",
    "api_url": "http://jants.janastu.org/annos/",
    "DEBUG": True,
    "HOST": '0.0.0.0'
   }	


# Cloudant database endpoint
# anno_api = "http://jants.janastu.org/annos/"


# what is this for?
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}


# Get list of annotations
@app.route('/annotations/api/v1.0/annos', methods=['GET'])
def get_annotations():
    api_req =  config['api_url']+"_all_docs"
    response = requests.get(api_req)
    response = response.json()
    return jsonify({'annotations': response['rows']})


# Get annotation with id = anno_id
@app.route('/annotations/api/v1.0/annos/<string:anno_id>', methods=['GET'])
def get_annotation(anno_id):
    api_req = config['api_url']+anno_id
    response = requests.get(api_req)
    if response.status_code == 404:
        abort(404)
    response = response.json()
    return jsonify({'annotation': response})


# Post new annotation
@app.route('/annotations/api/v1.0/annos', methods=['POST'])
def create_annotation():
    if not request.json or not 'body' in request.json:
        abort(400)
    annotation = request.get_json()
    auth=(config['key'], config['passphrase'])
    api_url = config['api_url']
    headers = {'content-type': 'application/json'}
    response = requests.post(api_url,data=json.dumps(annotation),headers=headers,auth=auth)
    return jsonify({'response': response.json(), 'annotation': annotation}), 201


# Update existing annotation
@app.route('/annotations/api/v1.0/annos/<string:anno_id>', methods=['PUT'])
def update_annotation(anno_id):
#to do: fetch annotation
    api_url = config['api_url']+anno_id
    response = requests.get(api_url)
    db_rev = response.headers.get('Etag')
    if response.status_code == 404:
        abort(404)
#validate annotation -- else send back errors
    if response.json().get('_id') != anno_id:
        abort(400)
    if not response.headers.get('Etag'):
        abort(400)
    if not request.json or not 'body' in request.json:
        abort(400)

#update fields
    auth=(config['key'], config['passphrase'])
    headers = {'content-type': 'application/json'}
    annotation = request.get_json()
    # refer to cloudant docs update api
    annotation['_rev'] = db_rev.strip('"')
    
#PUT DB
    putResp = requests.put(api_url,data=json.dumps(annotation),headers=headers,auth=auth)
    return jsonify({'response': putResp.json(), 'annnotation': annotation})


# Delete existing annotation
@app.route('/annotations/api/v1.0/annos/<string:anno_id>', methods=['DELETE'])
def delete_task(anno_id):
    auth=(config['key'], config['passphrase'])
    api_req = config['api_url']+anno_id
    headers = {'content-type': 'application/json'}
    r = requests.get(api_req)
    rev = r.json()['_rev']
    api_rev=api_req+'?rev='+rev
    response = requests.delete(api_rev)
    if response.status_code == 404:
        abort(404)
    return jsonify({'result': response.json() })


if __name__ == '__main__':
    app.run(debug=config['DEBUG'],host=config['HOST'])
