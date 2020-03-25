FROM python:3.7
COPY ./requirements.txt /dockerBuild/requirements.txt
WORKDIR /dockerBuild
RUN pip3 install -r requirements.txt
RUN black . --check
RUN black . --diff
RUN black .
COPY . /dockerBuild
CMD ["flask", "run", "--host", "0.0.0.0"]
