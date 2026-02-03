# settings.py

DATABASES = {
    'postgresql_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quickdb',
        'USER': 'sonarsource',
        'PASSWORD': '', # Noncompliant: Empty passwords should not be used in database configurations
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
