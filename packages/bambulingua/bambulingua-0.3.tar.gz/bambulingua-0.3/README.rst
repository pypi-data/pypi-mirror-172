======
lingua
======

lingua is a Django app to conduct web-based polls. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "lingua" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'lingua',
    ]

2. Include the lingua URLconf in your project urls.py like this::

    path('lingua/', include('lingua.urls')),

3. Run ``python manage.py migrate`` to create the lingua models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a lingua (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/lingua/ to participate in the poll.