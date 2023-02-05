FROM python:3.7.6

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV FLASK_APP batoken.py
WORKDIR /project
ADD ./app/ /project

ENV ABI=blockchain_conf/truffle/BAToken.json
ENV ACCOUNTS=blockchain_conf/ganache/addresses.json
ENV DB_DIR=/project/database/

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]