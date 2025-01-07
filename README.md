# Library Subject Guides LTI App

[![Build Status](https://github.com/uw-it-aca/library-guides-lti/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=master)](https://github.com/uw-it-aca/library-guides-lti/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/library-guides-lti/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/library-guides-lti?branch=master)

## Description
library-guides-lti is an LTI Tool built to display
UW Library Subject Guides for Canvas courses.

## Test Drive

To experience the tool in a development environment using mock data,
make sure docker is installed on your host and then run:
```
    # docker-compose up --build
```
Once built and running, you can start the LTI tool launch
sequence by visiting:
```
    http://your-host:8000/blti/dev
```
from your brower.
