FROM python:3.8


WORKDIR /code

ADD pkcs11-proxy /usr/local/lib/
ENV PKCS11_MODULE=/usr/local/lib/libpkcs11-proxy.so

COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple

# copy the content of the local src directory to the working directory
COPY ./ .

# command to run on container start
CMD [ "python3", "./app.py" ]

