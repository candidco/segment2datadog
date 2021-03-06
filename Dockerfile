FROM python:3.6
ARG GIT_SHA
ENV GIT_SHA=$GIT_SHA
ADD . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--log-file=-"]
