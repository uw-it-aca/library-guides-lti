# Library Subject Guides LTI App

[![Build Status](https://github.com/uw-it-aca/library-guides-lti/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=master)](https://github.com/uw-it-aca/library-guides-lti/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/library-guides-lti/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/library-guides-lti?branch=master)

A Django LTI Application for displaying Library Subject Guides in a Canvas course

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
