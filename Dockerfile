FROM python:2.7.12-alpine

# Dependencies
ENV MAGICK_HOME=/usr
RUN apk add --update git imagemagick imagemagick-dev

# copy required files
RUN mkdir /src
WORKDIR /src
COPY *.py /src/
COPY *.ini /src/
COPY requirements.txt /src/

# run pip install
#RUN pip install -r requirements.txt

# start the pipeline
CMD ["python","command_line.py", "-c", "config.ini"]
