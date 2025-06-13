# syntax=docker/dockerfile:1.12
# https://hub.docker.com/r/docker/dockerfile
# ======================================================================================================================
# Build Image:
# ------------
#
#   ...\> docker build -f ./Dockerfile -t illagrenan/django-asgi-lifespan .
#
# Run Image:
# ----------
#
#   ...\> docker run -p 127.0.0.1:8000:8000/tcp --rm -it illagrenan/django-asgi-lifespan
#
# ======================================================================================================================
FROM python:3.13.5-bookworm

ARG POETRY_EXTRA_OPTIONS=--with=dev,tests
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=60 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_CACHE_DIR="/opt/poetry/.cache"
SHELL ["/bin/bash", "-EeuxoC", "pipefail", "-c"]

RUN pip install --no-input "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.in-project true

WORKDIR /usr/src/app/
COPY ./django_asgi_lifespan /usr/src/app/django_asgi_lifespan/
COPY ./tests /usr/src/app/tests/
COPY pyproject.toml poetry.lock /usr/src/app/
RUN touch README.md
RUN --mount=type=cache,target=${POETRY_CACHE_DIR} \
    poetry install -vv ${POETRY_EXTRA_OPTIONS} --no-interaction --no-ansi
ENV PATH="/usr/src/app/.venv/bin:$PATH"

EXPOSE 8000
CMD [ "gunicorn", \
      "django_test_application.asgi:application", \
      "-b 0.0.0.0:8000", \
      "--workers=2", \
      "--worker-class=uvicorn.workers.UvicornWorker", \
      "--chdir=/usr/src/app/tests/", \
      "--log-level=debug" \
]
