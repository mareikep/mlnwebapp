import tempfile
from webmln.gui.app import mlnApp
import os
import jinja2
import logging
from logging import FileHandler


def ulogger(name): return logging.getLogger('userstats')

def init_webapp(app, db):
    print 'Initializing MLN webapp...'

    mlnApp.app = app
    # use html templates from mln app
    mln_loader = jinja2.ChoiceLoader([
        mlnApp.app.jinja_loader,
        jinja2.FileSystemLoader(['/opt/practools/tools/pracmln/webmln/gui/templates']),
    ])
    mlnApp.app.jinja_loader = mln_loader
    mlnApp.app.config['MLN_STATIC_PATH'] = '/opt/practools/tools/pracmln/webmln/gui/build'

    # settings for fileuploads and logging
    mlnApp.app.config['ALLOWED_EXTENSIONS'] = {'mln', 'db', 'pracmln', 'emln'}
    mlnApp.app.config['UPLOAD_FOLDER'] = '/home/ros/pracfiles'
    mlnApp.app.config['MLN_ROOT_PATH'] = '/opt/practools/tools/pracmln'
    mlnApp.app.config['EXAMPLES_FOLDER'] = os.path.join(mlnApp.app.config['MLN_ROOT_PATH'], 'examples')
    mlnApp.app.config['LOG_FOLDER'] = os.path.join('/opt/practools/tools/pracmln/webmln/gui/', 'log')

    if not os.path.exists(mlnApp.app.config['LOG_FOLDER']):
       os.mkdir(mlnApp.app.config['LOG_FOLDER'])

    ulog = logging.getLogger('userstats')
    ulog.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s,")
    filelogger = FileHandler(os.path.join(mlnApp.app.config['LOG_FOLDER'], "userstats.json"))
    filelogger.setFormatter(formatter)
    ulog.addHandler(filelogger)


    print 'Registering MLN routes...'
    from webmln.gui.pages import learning
    from webmln.gui.pages import inference
    from webmln.gui.pages import views
    from webmln.gui.pages import fileupload
    from webmln.gui.pages import utils
