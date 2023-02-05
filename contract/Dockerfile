FROM node:16-bullseye-slim as base

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        python3 && \
    rm -fr /var/lib/apt/lists/* && \
    rm -rf /etc/apt/sources.list.d/*

RUN npm install --global npm truffle ganache

FROM base as truffle

RUN mkdir -p /home/app
WORKDIR /home/app

COPY truffle-config.js /home/app
COPY contracts /home/app/contracts
COPY migrations /home/app/migrations/
COPY test /home/app/test/

CMD ["truffle", "deploy", "--reset"]

FROM base as ganache

RUN mkdir -p /home
WORKDIR /home
EXPOSE 8545

RUN mkdir -p shared
RUN touch shared/addresses.json

ENTRYPOINT ["ganache", "-h", "0.0.0.0", "--wallet.accountKeysPath", "shared/addresses.json"]