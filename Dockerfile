# Use an official Python runtime as a parent image
FROM python:3.12.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install python dependencies
COPY polystage_backend/requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copy project
COPY polystage_backend/ /code/

# Expose the port server will listen on
EXPOSE $PORT

# Command to run the app. Replace "myproject" with your project name
CMD ["gunicorn", "--bind", ":${PORT}", "polystage_backend.wsgi:application"]