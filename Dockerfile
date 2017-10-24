FROM python:2.7.12-alpine

# Dependencies
ENV MAGICK_HOME=/usr
RUN apk add --update git imagemagick imagemagick-dev

# copy required files
COPY src /src
WORKDIR /src
COPY requirements.txt /tmp/

# run pip install
RUN pip install -r /tmp/requirements.txt

# start the pipeline
CMD ["python","command_line.py", "-c", "config.ini"]
