# Select the base image
# Workdir
# Copy the req file
# install the package
# copy remain files
# Start the server

FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY send_email_server.py ./send_email_server.py

EXPOSE 8000
CMD [ "python","send_email_server.py" ]
