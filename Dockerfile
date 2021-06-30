FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .
CMD ["bash", "uvicorn", "app.main:app", "--reload", "--workers","1", "--host","0.0.0.0","--port", "8000"]