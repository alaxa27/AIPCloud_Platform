FROM python:3.5

# Copying the requirements for installation to take
# advantage of the caching.
RUN apt-get update && apt-get install -y sox
COPY requirements.txt .
RUN pip3 install -r ./requirements.txt
COPY requirements2.txt .
RUN pip3 install -r ./requirements2.txt
