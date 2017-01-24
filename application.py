import logging
import logging.handlers
import waterApplication
import os

from wsgiref.simple_server import make_server

if 'RDS_HOSTNAME' in os.environ:
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': os.environ['RDS_DB_NAME'],
      'USER': os.environ['RDS_USERNAME'],
      'PASSWORD': os.environ['RDS_PASSWORD'],
      'HOST': os.environ['RDS_HOSTNAME'],
      'PORT': os.environ['RDS_PORT'],
      }
    }


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
#LOG_FILE = '/opt/python/log/sample-app.log'
LOG_FILE = '/tmp/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

welcome =""
indexFile = "index.html"

def readHtmlFile(myfile):
  with open(myfile) as mf:
      fileContent = mf.read()
  return fileContent


def application(environ, start_response):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size).decode()
                logger.info("Received message: %s" % request_body)
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = welcome
        
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]


if __name__ == '__main__':

#    waterApplication.readConfigFile()
#    response , browser =  waterApplication.handleWaterLogin()
#    acctInfo =  waterApplication.getWaterAccountMain(response)

    welcome = readHtmlFile(indexFile)
    # welcome = readHtmlFile("wat.html")
    
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
