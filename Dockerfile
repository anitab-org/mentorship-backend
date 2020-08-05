FROM python:3.7
COPY ./pyproject.toml /dockerBuild/pyproject.toml
WORKDIR /dockerBuild
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN poetry install
COPY . /dockerBuild
CMD ["flask", "run", "--host", "0.0.0.0"]
