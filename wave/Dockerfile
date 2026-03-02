FROM python:3-alpine3.17

RUN addgroup -g 1002 appgroup && \
    adduser -D -u 1002 -G appgroup appuser

WORKDIR /var/www

ADD ./requirements.txt .

RUN pip install -r requirements.txt

ADD . /var/www

USER appuser

# define the port number the container should expose
EXPOSE 5000



CMD ["python", "app/run.py"]
