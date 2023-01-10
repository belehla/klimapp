FROM docker.io/python:3.9.5
RUN pip install flask==1.1.2
RUN pip install numpy==1.21.2
RUN pip install pandas==1.2.2
COPY . /src/
CMD ["python", "/src/klimapp.py"]


