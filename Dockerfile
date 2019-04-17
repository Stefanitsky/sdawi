FROM python:3.7-alpine

ENV SDAWI_VERSION 0.2.1

RUN apk add --no-cache --virtual .build-deps curl unzip \
      && python -m pip install --upgrade pip \
      && curl -Lo /tmp/sdawi.zip https://github.com/Stefanitsky/sdawi/archive/v${SDAWI_VERSION}.zip \
      && unzip /tmp/sdawi.zip -d /opt/ \
      && rm -f /tmp/sdawi.zip \
      && mkdir /etc/sdawi \
      && cd /opt/sdawi-${SDAWI_VERSION} \
      && pip install pipenv \
      && echo "Begin install sdawi" \
      && pipenv sync --sequential \
      && apk del .build-deps

EXPOSE 5000

WORKDIR /opt/sdawi-${SDAWI_VERSION}

ENTRYPOINT ["pipenv", "run", "python", "sdawi.py"]
