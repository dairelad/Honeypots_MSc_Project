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

#Add file to docker
COPY /ssh/sshHp.py /usr/src/app/ssh
COPY /telnet/telnetHp.py /usr/src/app/telnet
COPY /http/httpHp.py /usr/src/app/http
COPY /https/httpsHp.py /usr/src/app/https
COPY run.sh /usr/src/app

#Install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

#Made script executeable on cloud machine
#RUN chmod a+x /usr/src/app/run.sh

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.
CMD ["./run.sh"]

#Copy all contents from host working directory to docker working directory
COPY . .