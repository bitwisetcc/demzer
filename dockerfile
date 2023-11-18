FROM python:3.11-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN apk add --update --no-cache --virtual build-essential gcc libc-dev linux-headers nodejs npm mysql-dev bash
RUN pip install -r requirements.txt
RUN npm i
RUN npm run build
RUN python manage.py collectstatic --no-input
RUN chmod +x entrypoint.sh

CMD /app/entrypoint.sh
#CMD ["tail" , "-f", "/dev/null"]

EXPOSE 8080
