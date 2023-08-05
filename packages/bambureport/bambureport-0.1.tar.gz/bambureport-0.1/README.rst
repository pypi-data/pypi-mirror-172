======
report
======

report is a Django app to conduct web-based polls. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "report" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'report',
    ]

2. Include the report URLconf in your project urls.py like this::

    path('report/', include('report.urls')),

3. Run ``python manage.py migrate`` to create the report models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a report (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/report/ to participate in the poll.