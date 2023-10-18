# syntax=docker/dockerfile:1.4

FROM python:3.11-alpine
EXPOSE 8000
WORKDIR /app 

COPY . /app 

RUN apk add --update --no-cache --virtual build-essential gcc libc-dev linux-headers nodejs npm mysql-dev bash
RUN pip install -r requirements.txt
RUN npm i
RUN npm run build
RUN python manage.py collectstatic --no-input
RUN chmod +x entrypoint.sh

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
