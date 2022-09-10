FROM python:3

#Select working directory in container
WORKDIR /usr/src/app

#Make directories for honeypots
RUN mkdir ssh
RUN mkdir telnet
RUN mkdir http
RUN mkdir https

#Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Copy relevant files into docker container
#COPY /ssh/sshHp.py /usr/src/app/ssh
#COPY /telnet/telnetHp.py /usr/src/app/telnet
#COPY /http/httpHp.py /usr/src/app/http
#COPY /https/httpsHp.py /usr/src/app/https
#COPY parseLogs.py /usr/src/app
#COPY GeoLite2-City_20211102 /usr/src/app
#COPY crontab_file /usr/src/app
#COPY run.sh /usr/src/app

#Copy all contents from host working directory
#to docker working directory
COPY . .

#Install dependencies
RUN apt-get update
RUN apt-get -y install cron
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

#Give execution rights to the cron job

RUN chmod 0644 /usr/src/app/crontab_file
#Create the log file to be able to run tail
RUN crontab /usr/src/app/crontab_file

#Made script executeable
RUN chmod a+x /usr/src/app/run.sh
RUN chmod a+x /usr/src/app/parseLogs.py
RUN chmod a+x /usr/src/app/sendFiles.py

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.
CMD ["./run.sh"]