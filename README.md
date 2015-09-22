Library Subject Guides LTI App
===========================

A Django LTI Application for displaying Library Subject Guides in a Canvas course

Installation
------------

**Project directory**

Install grading-standard-lti in your project.

    $ cd [project]
    $ pip install -e git+https://github.com/uw-it-aca/library-guides-lti/#egg=libguide

Project settings.py
------------------

**INSTALLED_APPS**

    'libguide',
    'blti',

**BLTI settings**

[django-blti settings](https://github.com/uw-it-aca/django-blti#project-settingspy)

Project urls.py
---------------
    url(r'^libguide/', include('libguide.urls')),
