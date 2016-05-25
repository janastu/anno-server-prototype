# Annotation Server Prototype
Annotation server prototype specific to w3c annotation protocol as defined https://www.w3.org/TR/annotation-protocol at the time of this repo creation

# Specifications / Design / More
Read more about relevant specifications and whatever else emerges [here](https://github.com/janastu/anno-server-prototype/wiki)

## Installation
Like any flask application

### Step 1
Copy the contents of sample_config.py to new file config.py
  `cp sample_config.py config.py`

### Step 2 
Install dependencies from requirements.txt
  `pip install -r requirements.txt`

### Step 3
After the dependencies have successfully installed, run the server.py file
  `python run server.py`

If all went well, your application should be running at port 5000,
you should see something like below in your terminal.
  ` * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)`
