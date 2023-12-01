FROM python:3.9
LABEL authors="Konstantin.Chaika"

COPY requirements.txt LinksChecker/requirements.txt
RUN pip3 install -r LinksChecker/requirements.txt
COPY main.py LinksChecker/main.py

ENTRYPOINT ["python3h", "/LinksChecker/main.py"]
#CMD ["python3", "/LinksChecker/main.py", "--dir=/repo"]
