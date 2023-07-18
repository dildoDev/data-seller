FROM python:3-alpine

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

RUN pip3 install --upgrade pip
RUN pip3 install pyrogram tgcrypto uvloop

COPY . .

CMD ["python3", "main.py"]