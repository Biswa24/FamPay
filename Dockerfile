# start from an official image
FROM python:3.8-alpine

RUN mkdir -p /opt/assignment
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./assignment /opt/assignment
WORKDIR /opt/assignment

# expose the port 8000
EXPOSE 8001

ENV FLASK_ENV=development

CMD ["python3", "app.py", "-p 8001"]