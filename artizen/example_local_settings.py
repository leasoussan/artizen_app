# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Here you have secret Key '

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


EMAIL_HOST_USER = 'your Email'
EMAIL_HOST_PASSWORD = 'your Code -google code for more security '

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('BASE_DIR' , 'db.sqlite3'),
    }
}