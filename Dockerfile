FROM registry.access.redhat.com/ubi8/ubi:8.2

LABEL maintainer="Matthew F Leader <mleader@redhat.com>"

ENV PATH /root/.local/bin:$PATH \
    PIP_NO_CACHE_DIR off \
    APP_ROOT /data_server \
    LANG 'en_US.UTF-8'

RUN dnf install -y python36 \
    ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip \
    && dnf clean all \
    && pip install pipenv

COPY ./app ${APP_ROOT}/app
COPY Pipfile ${APP_ROOT}/
COPY ./start.bash ${APP_ROOT}/start.bash
WORKDIR ${APP_ROOT}

RUN pipenv install --skip-lock

CMD ["/usr/bin/bash", "./start.bash"]