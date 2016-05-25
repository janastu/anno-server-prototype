# Unit tests for annotation model implementation

from base64 import b64encode
from server import app
import os
import json
import unittest
import tempfile
import config
from flask import request


class annoTests(unittest.TestCase):

     # Annotation test conditions - for get list of annos request
     # without actual annotation content
     # Response codes assertion    
     def test_get_anno(self):
         # sends HTTP GET request to the application
         # on the specified path
         tester = app.test_client(self)
          
         result = tester.get('/annotations/api/v1.0/annos', content_type='application/ld+json') 
         # assert the status code of the response
         self.assertEqual(result.status_code, 200)



     # Annotation post request
     # Assert data structure and response codes
     def test_post_anno(self):

         tester = app.test_client(self)

         # validate payload
	 # auth=(config.API_KEY, config.API_SECRET)

	 headers = {
		 'Authorization': 'Basic ' + b64encode("{0}:{1}".format(config.USER_NAME, config.PASSWORD)),
		 'Content-Type': 'application/json'
	 }
	 annotation = {"body":
		{"text": "", "type": "TextualBody", "language": "en", "format": "text/html"}, 
		"motivation": "describing", 
		"target": 
		{"source": "", 
			"selector": 
			{"type": "TypeOfSelector"}
		},
		"generator": 
		{"homepage": "", 
			"type": "SoftwareAgent",
			"id": "",
			"name": ""}, 
		"creator": {"nick": "", "type": "Person", "id": "", "name": ""}, 
		"@context": "http://www.w3.org/ns/anno.jsonld", 
		"type": "Annotation"
		}

         result = tester.post('/annotations/api/v1.0/annos', data=json.dumps(annotation), headers=headers)

	 # Assert response codes
	 with app.test_request_context('/annotations/api/v1.0/annos', method='POST'):
 	     assert request.path == '/annotations/api/v1.0/annos'
	     assert request.method == 'POST'
         self.assertEqual(result.status_code, 201)

     
     # Annotation update request
     def test_put_anno(self):
         # validate payload
	 # send http put to server with payload
         # Assert response codes
         pass

     
     # Annotation Delete request
     def test_del_anno(self):
         # validate payload
	 # send http delete request
	 # Assert response codes
	 pass


if __name__ == '__main__':
    unittest.main()
