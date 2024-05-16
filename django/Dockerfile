# Use Python 3.11 base image (Alpine version)
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev mariadb-dev


# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
# Copy Django project files
COPY ./app /app

# Set work directory
WORKDIR /app

# Expose port (Django development server)
EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

# Command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]