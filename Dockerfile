FROM python:3.11-alpine@sha256:558d14432cef380aec99155f348ac1c5cb35072abf32209aecd5a8a422ff519a

ENV CRYPTOAUTHLIB_NOUSB=True

RUN apk update
RUN apk add --no-cache make
RUN apk add --no-cache gcc musl-dev linux-headers cmake libffi-dev
RUN apk add curl jq

# Set the working directory in the container
WORKDIR /app

COPY . /app

# Install the cryptoauthlib library
RUN pip install -r /app/requirements.txt

# Run the Python script when the container starts
CMD ["python", "/app/main.py"]