import sys
sys.path.insert(0, '/var/www/CRMaster.voice')

from app import app as application
application.secret_key = "someRandomSecretKey"