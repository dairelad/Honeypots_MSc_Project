FROM python:3

#Select working directory in container
WORKDIR /usr/src/app

#Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Add file to docker
COPY sshHp.py /usr/src/app
COPY telnetHp.py /usr/src/app
COPY httpHp.py /usr/src/app
COPY httpsHp.py /usr/src/app
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

COPY . .