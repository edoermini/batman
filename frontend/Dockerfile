FROM python:3.7.6

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD wait-for-deploy.py /

ENV FLASK_APP app.py
WORKDIR /project
ADD ./app/ /project


ENV BUILD=/project/blockchain_conf/truffle/BAToken.json
ENV ACCOUNTS=/project/blockchain_conf/ganache/addresses.json
ENV DB_DIR=/project/database/
ENV NODE_URL=http://ganache:8545

CMD ["flask", "run", "--host=0.0.0.0"]