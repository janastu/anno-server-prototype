# Unit tests for annotation model implementation


from server import app
import os
import json
import unittest
import tempfile


class annoTests(unittest.TestCase):

     # Annotation test conditions - for get request
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
         # validate payload 
         # send http post request to the server with payload
	 # Assert response codes
         pass


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
