from webmln.mlninit import mlnApp
import os
from os.path import expanduser
import jinja2
import logging
from logging import FileHandler

def register_routes():
    print 'Registering MLN routes...'
    from webrob.app_and_db import app
    
    mlnApp.app = app
    # use html templates from mln app
    mln_loader = jinja2.ChoiceLoader([
        mlnApp.app.jinja_loader,
        jinja2.FileSystemLoader([
            '/opt/practools/tools/pracmln/mlnGUI/webmln/templates']),
    ])
    mlnApp.app.jinja_loader = mln_loader
    mlnApp.app.secret_key = 'so secret!'
    mlnApp.app.config['MLN_STATIC_PATH'] = \
        '/opt/practools/tools/pracmln/mlngui/webmln/build'

    # settings for fileuploads and logging
    home = expanduser("~")
    mlnApp.app.config['ALLOWED_EXTENSIONS'] = set(['mln','db','pracmln','emln'])
    mlnApp.app.config['UPLOAD_FOLDER'] = os.path.join(home, 'mlnfiles')
    mlnApp.app.config['EXAMPLES_FOLDER'] = '/opt/practools/tools/pracmln/examples'
    mlnApp.app.config['MLN_ROOT_PATH'] = '/opt/practools/tools/pracmln'
    mlnApp.app.config['LOG_FOLDER'] = os.path.join(mlnApp.app.config['UPLOAD_FOLDER'], 'log')

    if not os.path.exists(mlnApp.app.config['UPLOAD_FOLDER']):
       os.mkdir(mlnApp.app.config['UPLOAD_FOLDER'])

    if not os.path.exists(mlnApp.app.config['LOG_FOLDER']):
       os.mkdir(mlnApp.app.config['LOG_FOLDER'])

    ulog = logging.getLogger('userstats')
    ulog.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s,")
    filelogger = FileHandler(os.path.join(mlnApp.app.config['LOG_FOLDER'], "logs.json"))
    filelogger.setFormatter(formatter)
    ulog.addHandler(filelogger)


    from webrob.pages import log
    from webmln.pages import learning
    from webmln.pages import inference
    from webmln.pages import views
    from webmln.pages import fileupload
    from webmln.pages import utils
