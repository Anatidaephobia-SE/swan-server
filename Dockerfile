FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /swan
COPY requirements.txt /swan/
RUN pip install -r requirements.txt
COPY . /swan/
RUN chmod +x /swan/swan-entrypoint.sh

ENTRYPOINT [ "/swan/swan-entrypoint.sh" ]