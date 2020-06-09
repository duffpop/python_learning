FROM python:alpine3.7
COPY . /plex_preroll
WORKDIR /plex_preroll
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD python3 ./preroll.py
