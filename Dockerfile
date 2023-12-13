FROM python:3.10.6-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /back


RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends vim && \
    apt-get install -y --no-install-recommends netcat && \
    apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev gcc git libpq-dev

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install 'pydantic[email]'

RUN pip3 install --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip3 install --trusted-host pypi.org --no-cache-dir -r /tmp/requirements.txt


RUN rm -rf /tmp/requirements.txt && \
    apt-get autoremove -y --purge && \
    apt-get clean -y

RUN useradd -m -s /bin/bash -d /home/managing_user  managing_user && \
    chown -R managing_user:managing_user /back

USER managing_user
WORKDIR /app

CMD ["python3", "main.py"]

