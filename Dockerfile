FROM python:3.10.11
WORKDIR /docker_imse_m2_group6
ADD . /docker_imse_m2_group6
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
