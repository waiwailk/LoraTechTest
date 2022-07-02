FROM python:3-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

COPY . /app


ENTRYPOINT [ "python" ]

CMD ["view.py" ]