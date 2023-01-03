FROM docker.io/python:3.9.5
RUN pip install flask==1.1.2
COPY . /src/
CMD ["python", "/src/klimapp.py"]


