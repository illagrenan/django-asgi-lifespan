
# syntax=docker/dockerfile:1.17
FROM python:3.13.5-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ARG UV_EXTRA_OPTIONS=--group=dev
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
SHELL ["/bin/bash", "-EeuxoC", "pipefail", "-c"]

WORKDIR /usr/src/app/

# Install only external dependencies (cached layer)
RUN --mount=type=cache,target=/opt/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --all-groups \
        --no-install-project

# Copy source and install local package in development mode
COPY pyproject.toml uv.lock README.md /usr/src/app/
COPY ./django_asgi_lifespan /usr/src/app/django_asgi_lifespan/
COPY ./tests /usr/src/app/tests/

RUN --mount=type=cache,target=/opt/.cache/uv \
    uv sync \
        --locked \
        --all-groups \
        --no-editable

EXPOSE 8000
CMD [ "uv", "run", "gunicorn", \
      "django_test_application.asgi:application", \
      "-b", "0.0.0.0:8000", \
      "--workers=2", \
      "--worker-class=uvicorn.workers.UvicornWorker", \
      "--chdir=/usr/src/app/tests/", \
      "--log-level=debug" \
]
