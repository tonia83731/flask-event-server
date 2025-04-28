FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev mariadb-dev && \
    rm -rf /var/cache/apk/*

# Copy the project files into the container
COPY . /app 

COPY .env.dev /app/.env.dev

# Create virtual environment
RUN python -m venv .env

# Activate the virtual environment and install Python dependencies
RUN . .env/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Set environment variables for flask
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development

# Expose the flask app port
EXPOSE 5000

CMD ["/bin/sh", "-c", ". .env/bin/activate && flask run --host=0.0.0.0"]




