FROM python:3.8

RUN pip install --index-url http://armbjs:xkqfhf12@docker.armbjs.com:8080/simple/ fake_pubsub_m --no-cache-dir --trusted-host docker.armbjs.com:8080

CMD ["python", "-m", "fake_pubsub_m"]