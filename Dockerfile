FROM python:3.7.3-alpine3.9

ENV SDAWI_VERSION 0.2.2

RUN apk update \
      && apk add --no-cache postgresql-dev \
      && apk add --no-cache --virtual .build-deps curl unzip musl-dev gcc python3-dev \
      && python -m pip install --upgrade pip \
      && curl -Lo /tmp/sdawi.zip https://github.com/Stefanitsky/sdawi/archive/v${SDAWI_VERSION}.zip \
      && unzip /tmp/sdawi.zip -d /opt/ \
      && rm -f /tmp/sdawi.zip \
      && mkdir /etc/sdawi \
      && cd /opt/sdawi-${SDAWI_VERSION} \
      && echo "Begin install sdawi" \
      && pip install -r requirements.txt \
      && apk del .build-deps \
      && echo Done

EXPOSE 5000

WORKDIR /opt/sdawi-${SDAWI_VERSION}

ENTRYPOINT ["pipenv", "run", "python", "sdawi.py"]
