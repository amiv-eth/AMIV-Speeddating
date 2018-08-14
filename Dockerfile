FROM python:3.6-alpine

# Create user with home directory and no password and change workdir
RUN adduser -Dh /speeddating speeddating
WORKDIR /speeddating

EXPOSE 8080

# Install bjoern and dependencies for install (we need to keep libev)
RUN apk add --no-cache --virtual .deps \
        musl-dev python-dev gcc git && \
    apk add --no-cache libev-dev libffi libffi-dev openssl openssl-dev && \
    pip install bjoern

# Copy files to /api directory, install requirements
COPY ./ ./
RUN pip install -r ./requirements.txt

# Cleanup dependencies
RUN apk del .deps

# Switch user
USER speeddating

# Start bjoern
CMD ["python3", "server.py"]
