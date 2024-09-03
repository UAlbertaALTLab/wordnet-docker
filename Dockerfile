# Based on the process to make speech-db

FROM python:3.10 AS builder
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --dev

RUN apt-get update -qq && apt-get -y install curl unzip
RUN mkdir /app/nltk_data
RUN curl https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet31.zip -o nltk_data/wordnet31.zip
RUN mkdir -p -v /app/nltk_data/corpora/
RUN unzip nltk_data/wordnet31.zip -d /app/nltk_data/corpora/
RUN mv -v /app/nltk_data/corpora/wordnet31 /app/nltk_data/corpora/wordnet

FROM python:3.10
ARG UID_GID=60005
ARG WSGI_USER=wordnet
RUN groupadd --system --gid ${UID_GID} ${WSGI_USER} \
 && useradd --no-log-init --system --gid ${WSGI_USER} --uid ${UID_GID} ${WSGI_USER} \
 && mkdir /app \
 && mkdir /app/nltk_data \
 && chown ${WSGI_USER}:${WSGI_USER} /app /app/nltk_data

 USER ${WSGI_USER}:${WSGI_USER}
 WORKDIR /app/

 COPY --from=builder --chown=${WSGI_USER}:${WSGI_USER} /app/.venv /app/.venv
 COPY --from=builder --chown=${WSGI_USER}:${WSGI_USER} /app/nltk_data /app/nltk_data
 COPY --chown=${WSGI_USER}:${WSGI_USER} . .
 ENV VIRTUAL_ENV="/app/.venv"
 ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

 EXPOSE 8000
 ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_KEEPALIVE=0 UWSGI_AUTO_CHUNKED=1 UWSGI_WSGI_ENV_BEHAVIOUR=holy
 CMD ["uwsgi", "-w", "wordnet.wsgi", "--processes", "2"]
