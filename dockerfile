FROM python:3.11-slim

# Code here is executed as root

RUN useradd -u 8879 -m calici
RUN mkdir /app
RUN chown -R calici:calici /app
RUN pip install https://github.com/Calici/module-api/releases/download/vNightly/module_api-0.0.26-py3-none-any.whl
# Code here is executed as user

# Code after this is just preparation for running
WORKDIR /app
COPY ./src /app
ENTRYPOINT ["python3", "/app/run.py"]