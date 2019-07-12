#downloading the base image alpine
FROM ubuntu:18.04

RUN groupadd docker
RUN useradd edukauser
RUN usermod -a -G docker edukauser



# install python3 and pip3 then upgrade the pop so
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev


RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            tzdata \
        && rm -rf /var/lib/apt/lists/*


## To install pgcog2 for postgres
RUN apt-get update -y && \
    apt-get install -y python3-psycopg2

## To install Pillow we need to install the following
RUN apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev \
    tcl8.6-dev tk8.6-dev python-tk \
    && rm -rf /var/lib/apt/lists/*


# copy the source code of the flask app: eduka
# create a app folder inside the docker image
WORKDIR /app

# we will be able to install the softwares in requirements.txt
COPY requirements.txt requirements.txt


RUN apt-get update -y && \
    apt-get install -y python3-venv

RUN python3 -m venv venv

# install the softwares in the requirements.txt
# in the image
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

# copy the source code from the app on the computer
# to the app folder in the image
COPY eduka eduka
COPY migrations migrations
COPY app.py boot.sh ./
RUN chmod +x boot.sh


ENV FLASK_APP app.py

RUN chown -R edukauser:edukauser ./
USER edukauser

# expose the following port to access the app
# from outside the image
EXPOSE 5000

# make the entry point for the image
ENTRYPOINT ["./boot.sh"]

# the file that need to run first
# for the app to start
