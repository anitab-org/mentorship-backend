FROM python:3.7
COPY ./requirements.txt /dockerBuild/requirements.txt
WORKDIR /dockerBuild
RUN pip install -r requirements.txt
COPY . /dockerBuild
CMD ["flask", "run", "--host", "0.0.0.0"]
