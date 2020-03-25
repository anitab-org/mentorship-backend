FROM python:3.7
COPY ./requirements.txt /dockerBuild/requirements.txt
WORKDIR /dockerBuild
RUN pip3 install -r requirements.txt
COPY . /dockerBuild
RUN black /dockerBuild
CMD ["flask", "run", "--host", "0.0.0.0"]
