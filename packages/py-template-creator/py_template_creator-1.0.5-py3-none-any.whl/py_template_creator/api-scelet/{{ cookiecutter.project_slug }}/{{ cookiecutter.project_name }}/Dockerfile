ARG PYTHON_VERSION=3.10-slim

# Stage 0, instaling dev packages
FROM python:${PYTHON_VERSION} as builder
LABEL maintainer="Nebojsa Mrkic <mrkic.nebojsa@gmail.com>"
ENV PYTHONUNBUFFERED 1
ARG APP_DIR
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

WORKDIR /wheels
COPY ./$APP_DIR/requirements/ /wheels/requirements/
RUN pip install -U pip && pip wheel -r ./requirements/prod.txt

# Stage 1, no dev packages on wheels
FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1
ARG APP_DIR
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

COPY --from=builder /wheels /wheels
RUN pip install -U pip \
       && pip install -r /wheels/requirements/prod.txt \
                      -f /wheels \
       && rm -rf /wheels \
       && rm -rf /root/.cache/pip/*


# Copy code to docker
COPY ./$APP_DIR/ /opt/app/
COPY ./$APP_DIR/config/ /opt/app/config/
RUN mkdir -p /opt/app/running
WORKDIR /opt/app
RUN python setup.py install
# Collect our static media.

# Specify the command to run when the image is run.
CMD "/opt/app/config/run.sh"