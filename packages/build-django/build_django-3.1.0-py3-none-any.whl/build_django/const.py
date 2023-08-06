GITIGNORE: str = '/venv\n/static\n/media\n__pycache__\n*.sqlite*\n*.log\n.env'

ENV_EXAMPLE: str = '''
SECRET_KEY=

# List of comma separated values
ALLOWED_HOSTS=

# Remove if production
DEBUG=

# Sets SECURE_PROXY_SSL_HEAD to ('HTTP_X_FORWARDED_PROTO', 'https')
# Remove if not needed
USE_SSL=
'''

DEFAULT_ENV = '''
    DEBUG=(bool, False),
    USE_SSL=(bool, False)
'''

REQUIRED_PACKAGES: list[str] = (
    'wheel',
    'django',
    'django-environ',
    'gunicorn'
)
