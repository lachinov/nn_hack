FROM fenixfly/vinodock
USER root
WORKDIR /

RUN pip3 install aiohttp torch typing

COPY . /app

ENTRYPOINT [ "bash" , "-l", "-c" ]

CMD [ "cd /app && /usr/bin/python3 api.py" ]
