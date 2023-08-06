
##### BASE Build #####
# pull official base image
ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim as base

LABEL fm.trove.image.name="Trove Farmer's Market"
LABEL fm.trove.image.authors="Brian Farrell <brian.farrell@me.com>"

# create virtual environment
ENV VIRTUAL_ENV=/opt/trove-fm
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set environment variables
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc git postgresql libpq-dev \
  && apt-get clean


##### TEST Build #####
FROM base AS test

COPY ../run_prod.py /run.py

# install python dependencies
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install "trove-fm[test] @ git+https://gitlab.com/brianfarrell/trove-fm.git"

CMD ["/opt/trove-fm/bin/python",  "-m", "run"]


##### PROD Build #####
FROM base AS prod

COPY ../run_prod.py /run.py

# install python dependencies
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install "git+https://gitlab.com/brianfarrell/trove-fm.git"

CMD ["/opt/trove-fm/bin/python",  "-m", "run"]


##### DEV Build #####
FROM base AS dev

ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /app

COPY ../ $WORKDIR

# install python dependencies for DEV environment
RUN export SETUPTOOLS_SCM_PRETEND_VERSION=$(python -c "from trove_fm._version import version; print(f'{version}')") \
    && $VIRTUAL_ENV/bin/pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install -e .[test,doc]
