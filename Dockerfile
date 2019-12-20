FROM python:3.7

# RUN apk add --no-cache python3-dev \
#     && pip3 install --upgrade pip

# RUN ls

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]