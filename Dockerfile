FROM python:3.7.10
ENV PYTHONUNBUFFERED=1
WORKDIR /swan
COPY requirements.txt /swan/
RUN pip install -r requirements.txt
COPY . /swan/
RUN chmod +x /swan/swan-entrypoint.sh 
RUN apt-get update && \
    apt-get install dos2unix && \
    apt-get clean
RUN dos2unix /swan/swan-entrypoint.sh

ENTRYPOINT [ "/bin/bash","/swan/swan-entrypoint.sh" ]