Django telemetry
----------------

.. image:: /django_telemetry/static/telemetry/img/logo.png
  :width: 50
  :alt: Alternative text

This package is used to monitor and manage requests

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_telemetry" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_telemetry',
    ]

2. Include the telemetry URLconf in your project urls.py like this::

    path('telemetry/', include('django_telemetry.urls')),

3. Add 'django_telemetry.middleware.WebTelemetryMiddleware', middleware in settings.py like this::

    MIDDLEWARE = [
        ...
        'django_telemetry.middleware.WebTelemetryMiddleware',
    ]

4. Add second database in you settings.py file like this::

    DATABASES = {
        'default': {
            ...
        },
        
        'django_telemetry': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.telemetry.sqlite3',
        }
    }

5. Add DATABASE_ROUTERS to settings.py like this::

    DATABASE_ROUTERS = ['django_telemetry.routers.DatabaseForTelemetry']

6. Run ``python manage.py migrate --database=django_telemetry`` to create the django_telemetry models.

7. Start the development server and visit http://127.0.0.1:8000/telemetry/
