# SECURITY WARNING: keep the secret key used in production secret!
# Import secret key from text file from different location on openshift environment and local environment

import os

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
	ON_OPENSHIFT = True

secret_key_dir = os.path.dirname(os.path.realpath(__file__))
if ON_OPENSHIFT:
	secret_key_dir = os.environ['OPENSHIFT_DATA_DIR']

with open(os.path.join(secret_key_dir, 'secret_key.txt')) as f:
	MY_SECRET_KEY = f.read().strip()

default_keys = { 'SECRET_KEY': MY_SECRET_KEY }
