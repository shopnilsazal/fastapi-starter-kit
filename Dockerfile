FROM python:3.14.3-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_LINK_MODE="copy" \
    APP_USERNAME="app_user" \
    USER_HOME="/home/app_user"

RUN apt-get update && \
    apt-get install -yq --no-install-recommends tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Dhaka /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    pip install --no-cache-dir --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash ${APP_USERNAME}

WORKDIR ${USER_HOME}/code
RUN chown -R ${APP_USERNAME}:${APP_USERNAME} ${USER_HOME}/code

USER ${APP_USERNAME}
ENV PATH="${USER_HOME}/.local/bin:${PATH}"

COPY --chown=${APP_USERNAME}:${APP_USERNAME} pyproject.toml uv.lock README.md ${USER_HOME}/code/

RUN uv pip install --prefix ${USER_HOME}/.local .
COPY --chown=${APP_USERNAME}:${APP_USERNAME} . ${USER_HOME}/code/
