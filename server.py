#! /usr/bin/python3

# A web annotation server based on LDP Protocol (http://www.w3.org/TR/2016/WD-annotation-protocol-20160331/)
# Things to do:
# Handle credentials by factoring them out of this code
# Implement containers based on LPD (https://www.w3.org/TR/ldp-primer/)
#   start with Basic Container implementation
#   only annotaitons will be stored in an annotation Container
#   test with annotations for a given context (place, document, ... )


from __future__ import print_function
import sys
from flask import Flask, jsonify, abort, make_response, request
import requests
import cloudant
import json
import jsonschema
from jsonschema import validate
import config


app = Flask(__name__)


# what is this for?
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}


# Get list of annotations
# @todo implement the BasicContainer for annotations to group them
@app.route('/annotations/api/v1.0/annos', methods=['GET'])
def get_annotations():
    api_req =  config.DATABASE_URL+"_all_docs"
    response = requests.get(api_req)
    response = response.json()
    print (config.API_KEY+"PRINT COMMAND")
    return jsonify({'annotations': response['rows']})


# Get annotation with id = anno_id
@app.route('/annotations/api/v1.0/annos/<string:anno_id>', methods=['GET'])
def get_annotation(anno_id):
    api_req = config.DATABASE_URL+anno_id
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
    auth=(config.API_KEY, config.API_SECRET)
    api_url = config.DATABASE_URL
    headers = {'content-type': 'application/json'}
    response = requests.post(api_url,data=json.dumps(annotation),headers=headers,auth=auth)
    return jsonify({'response': response.json(), 'annotation': annotation}), 201


# Update existing annotation
@app.route('/annotations/api/v1.0/annos/<string:anno_id>', methods=['PUT'])
def update_annotation(anno_id):
#to do: fetch annotation
    api_url = config.DATABASE_URL+anno_id
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
    auth=(config.API_KEY, config.API_SECRET)
    headers = {'content-type': 'application/json'}
    annotation = request.get_json()
    # refer to cloudant docs update api
    annotation['_rev'] = db_rev.strip('"')

#PUT DB
    putResp = requests.put(api_url,data=json.dumps(annotation),headers=headers,auth=auth)
    return jsonify({'response': putResp.json(), 'annnotation': annotation})


# Delete annotation with id anno_id
# Note that Cloudant insists on knwoing the revision of a resource, so revision must be included in call.
# Cloudant never really deletes any resource, just flags it.
@app.route('/annotations/api/v1.0/annos/<string:anno_id>', methods=['DELETE'])
def delete_task(anno_id):
    auth=(config.API_KEY, config.API_SECRET)
    api_url = config.DATABASE_URL+anno_id
    headers = {'content-type': 'application/json'}
    r = requests.get(api_url)
    rev = r.json()['_rev']
    api_rev=api_url+'?rev='+rev
    response = requests.delete(api_rev)
    if response.status_code == 404:
        abort(404)
    return jsonify({'result': response.json() })


if __name__ == '__main__':
    app.run(debug=config.DEBUG,host=config.HOST)
