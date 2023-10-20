FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN apk add --update --no-cache --virtual build-essential gcc libc-dev linux-headers nodejs npm mysql-dev

RUN pip install -r requirements.txt
RUN npm i
RUN chmod +x entrypoint.sh

CMD /app/entrypoint.sh
