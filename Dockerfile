FROM python:3.9 as build

RUN python -m pip install pip==19.3.1

ADD https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /get-poetry.py
ENV POETRY_HOME /pypoetry
RUN python /get-poetry.py \
  --yes \
  --force

ADD . /source
WORKDIR /source

RUN $POETRY_HOME/bin/poetry export \
  --format requirements.txt \
  --output /requirements.txt \
  --without-hashes \
  --extras deployment
RUN python -m pip wheel \
  --wheel-dir /wheels \
  --requirement /requirements.txt \
  --disable-pip-version-check \
  --no-cache-dir
RUN mv /source/openapi.yaml /source/kodak/openapi.yaml
RUN $POETRY_HOME/bin/poetry build \
  --format wheel
RUN mv /source/dist/*.whl /wheels


FROM python:3.9-slim as runtime

RUN apt update --yes && \
  apt install --yes \
    libjpeg-dev \
    zlib1g \
    liblcms2-2 && \
  apt clean all --yes && \
  python -m pip install pip==19.3.1 && \
  useradd kodak \
    --no-create-home \
    --no-log-init \
    --system \
    --user-group && \
  mkdir --parents /kodak/pictures && \
  mkdir --parents /kodak/content && \
  chown --recursive kodak:kodak /kodak && \
  chmod 0775 /kodak /kodak/content

COPY --from=build /wheels /wheels
RUN python -m pip install kodak[deployment] \
    --upgrade \
    --pre \
    --no-index \
    --no-cache-dir \
    --find-links /wheels \
    --disable-pip-version-check && \
  rm --recursive --force /wheels

ENV KODAK_SOURCE_DIR /pictures
ENV KODAK_CONTENT_DIR /kodak/content
ENV KODAK_DATABASE_SQLITE_PATH /kodak/kodak.db

VOLUME /kodak
VOLUME /pictures

USER kodak

CMD [ \
  "python", \
  "-m", \
  "gunicorn", \
  "kodak.application:APPLICATION", \
  "--bind=0.0.0.0:8080", \
  "--workers=8", \
  "--log-level=info", \
  "--access-logfile=-" \
]
