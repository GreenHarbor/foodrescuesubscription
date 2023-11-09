FROM --platform=linux/arm64 python:3.11-slim

WORKDIR /usr/app

COPY ./ /usr/app/

RUN mkdir /usr/app/logs

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "src/app.py"]
