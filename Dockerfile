ARG PYTHON_VERSION=3.8
FROM docker.io/python:${PYTHON_VERSION}-alpine as builder

##
## Build libolm for matrix-nio e2e support
##

# Install libolm build dependencies
ARG LIBOLM_VERSION=3.2.16
RUN apk add --no-cache \
    make \
    cmake \
    gcc \
    g++ \
    git \
    libffi-dev \
    yaml-dev \
    python3-dev

# Build libolm
#
# Also build the libolm python bindings and place them at /python-libs
# We will later copy contents from both of these folders to the runtime
# container
COPY docker/build_and_install_libolm.sh /scripts/
RUN /scripts/build_and_install_libolm.sh ${LIBOLM_VERSION} /python-libs

# Install native runtime dependencies
RUN apk add --no-cache \
    postgresql-dev \
    musl-dev

# Install python runtime modules. We do this before copying the source code
# such that these dependencies can be cached
# This speeds up subsequent image builds when the source code is changed
RUN mkdir -p /app/support_bot
COPY ./dependencies/support-bot/support_bot/__init__.py /app/support_bot/
COPY ./dependencies/support-bot/README.md ./support_bot/main.py /app/

# Build the dependencies
RUN pip install --upgrade pip
# Pin poetry version so updates don't break the build
RUN pip install poetry==1.8.2

# Disable poetry venv creation in builder.
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0

WORKDIR /app/dependencies/support_bot/
COPY ./dependencies/support-bot/pyproject.toml ./dependencies/support-bot/poetry.lock /app/dependencies/support_bot/

# Export poetry.lock to requirements file omitting hashes for faster dependency resolution
# And building libraries in external folder /python-libs
RUN poetry export --without-hashes --without dev --format=requirements.txt > requirements.txt
# Install production dependencies
RUN pip install --prefix="/python-libs" --ignore-installed --no-warn-script-location -r requirements.txt

# Setup Django dependencies for web app
WORKDIR /app/
COPY requirements.txt .
RUN pip install --prefix="/python-libs" --ignore-installed --no-warn-script-location -r requirements.txt

##
## Creating the runtime container
##

# Create the container we'll actually ship. We need to copy libolm and any
# python dependencies that we built above to this container
FROM docker.io/python:${PYTHON_VERSION}-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy python dependencies from the "builder" container
COPY --from=builder /python-libs /usr/local

# Copy libolm from the "builder" container
COPY --from=builder /usr/local/lib/libolm* /usr/local/lib/

# Install any native runtime dependencies
RUN apk add --no-cache \
    libstdc++ \
    libpq

WORKDIR /app/

# Now copy the source code for support_bot
COPY ./dependencies/support-bot/*.py ./dependencies/support-bot/*.md /app/support_bot/
COPY ./dependencies/support-bot/support_bot /app/dependencies/support_bot/support_bot/
COPY ./dependencies/support-bot/grpc_server/ /app/dependencies/support_bot/grpc_server/
COPY ./dependencies/support-bot/proto/ /app/dependencies/support_bot/proto/

# Copy project files
COPY *.py *.md /app/
COPY ./core/ /app/core/
COPY ./home/ /app/home/
COPY ./static/ /app/static/
COPY ./templates/ /app/templates/
COPY ./support_lib/ /app/support_lib/
# Copy linked files
COPY ./support_bot/ /app/support_bot/
COPY ./proto/ /app/proto/
# Copy django configs and launch files
COPY manage.py render.yaml /app/
COPY startup.sh /app/

# Specify a volume that holds the config file, SQLite3 database,
# and the matrix-nio store
VOLUME ["/data"]

# Startup script
#CMD tail -f /dev/null
ENTRYPOINT [ "/app/startup.sh" ]