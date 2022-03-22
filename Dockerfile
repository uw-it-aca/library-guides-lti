FROM gcr.io/uwit-mci-axdd/django-container:1.3.3 as app-container

ADD --chown=acait:acait libguide/VERSION /app/libguide/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/

RUN . /app/bin/activate && pip install -r requirements.txt

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

RUN . /app/bin/activate && pip install nodeenv && nodeenv -p &&\
    npm install -g npm && ./bin/npm install -g less

RUN . /app/bin/activate && python manage.py collectstatic --noinput &&\
    python manage.py compress -f

FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.3 as app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
